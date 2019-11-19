from functools import reduce

from django.utils import timezone
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import generics, status, serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from moca.models import User, Device, PaymentProfile, Issue, NoteImage
from moca.models.appointment import Appointment, AppointmentRequest, AppointmentCancellation, Note
from moca.services.notification.push import send_push_message
from moca.services.stripe import charge_customer

from ..user.permissions import IsObjectTherapistSelfOrReadonly
from .permissions import CanCancel, CanStart, CanEnd
from .serializers import (AppointmentCreateUpdateSerializer, AppointmentSerializer, NoteSerializer,
                          NoteImageSerializer)


class AppointmentListView(generics.ListAPIView):
  serializer_class = AppointmentSerializer

  def get_queryset(self):
    query_params = self.request.query_params
    user = self.request.user
    user_profile_model = user.get_profile_model()
    user_profile_type = user.get_profile_type()
    user_profile = user_profile_model.objects.get(user=user)

    filter_dict = {user_profile_type: user_profile}
    queries = [Q(**filter_dict)]

    start = query_params.get("start")
    if start:
      queries.append(Q(start_time__gte=start))

    end = query_params.get("end")
    if end:
      queries.append(Q(end_time__lte=end))

    hide_finished = query_params.get("hideFinished")
    only_finished = query_params.get("onlyFinished")

    if hide_finished == "true":
      queries.append(~Q(status="cancelled") & ~Q(status="completed") & ~Q(status="payment-failed"))
    if only_finished == "true":
      queries.append(Q(status="cancelled") | Q(status="completed") | Q(status="payment-failed"))

    query = reduce(lambda x, y: x & y, queries)

    limit = query_params.get("limit")
    if (limit):
      parsed_limit = int(limit)
      order_by = "-end_time" if parsed_limit < 0 else "start_time"
      return Appointment.objects.filter(query).order_by(order_by)[:abs(parsed_limit)]

    return Appointment.objects.filter(query)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'appointment_id'
  queryset = Appointment.objects.all()

  def get_serializer_class(self):
    if self.request.method == 'GET':
      return AppointmentSerializer
    else:
      return AppointmentCreateUpdateSerializer


class AppointmentNoteView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'appointment_id'
  serializer_class = NoteSerializer
  permission_classes = [IsObjectTherapistSelfOrReadonly]
  parser_classes = (MultiPartParser,)

  def get_object(self):
    appointment_id = self.kwargs.get(self.lookup_url_kwarg)
    instance, _ = Note.objects.get_or_create(appointment_id=appointment_id)

    return instance


class AppointmentNoteImageDestroyView(generics.DestroyAPIView):
  lookup_url_kwarg = 'image_id'
  queryset = NoteImage
  serializer_class = NoteImageSerializer
  # TODO: permission_classes = []


class AppointmentRequestView(APIView):
  def post(self, request, appointment_request_id, request_status):
    try:
      appointment_request = AppointmentRequest.objects.get(pk=appointment_request_id)
    except AppointmentRequest.DoesNotExist:
      raise APIException('Invalid appointment request')

    current_status = appointment_request.status

    if current_status != 'pending':
      raise APIException('Appointment request already handled')

    if request_status == 'accept':
      if self.request.user.id != appointment_request.patient_id:
        raise APIException('Only patient can accept')

      appointment_request.status = 'accepted'
      appointment_to_create = model_to_dict(appointment_request)
      appointment_to_create['status'] = 'not-started'

      serializer = AppointmentCreateUpdateSerializer(data=appointment_to_create)

      if serializer.is_valid():
        created_appointment = serializer.save()
        serialized_created_appointment = AppointmentSerializer(created_appointment,
                                                               context={
                                                                 'request': request
                                                               }).data
        appointment_request.save()

        devices = Device.objects.filter(user=appointment_request.therapist.user)
        text = f'Your appointment request for {request.user.first_name} {request.user.last_name} was accepted.'

        for device in devices:
          send_push_message(device.token, text, {
            'type': 'new_message',
            'params': {
              'user': {
                'id': request.user.id
              }
            }
          })

        return Response(serialized_created_appointment, status.HTTP_200_OK)

      else:
        raise APIException('Appointment request handler issue')

    elif request_status == 'reject':
      appointment_request.status = 'rejected'
      appointment_request.save()

      devices = Device.objects.filter(user=appointment_request.therapist.user)
      text = f'Your appointment request for {request.user.first_name} {request.user.last_name} was rejected.'

      for device in devices:
        send_push_message(device.token, text, {
          'type': 'new_message',
          'params': {
            'user': {
              'id': request.user.id
            }
          }
        })
      return Response("Rejected", status=status.HTTP_200_OK)

    elif request_status == 'cancel':
      if self.request.user.id != appointment_request.therapist_id:
        raise APIException('Only therapist can cancel')
      appointment_request.status = 'cancelled'
      appointment_request.save()

      devices = Device.objects.filter(user=appointment_request.patient.user)
      text = f'Your appointment with {request.user.first_name} {request.user.last_name} was cancelled.'

      for device in devices:
        send_push_message(device.token, text, {
          'type': 'new_message',
          'params': {
            'user': {
              'id': request.user.id
            }
          }
        })
      return Response("Cancelled", status=status.HTTP_200_OK)

    else:
      raise APIException('Incorrect request status')


class AppointmentCancellationSerializer(serializers.ModelSerializer):
  class Meta:
    model = AppointmentCancellation
    fields = ['type']


class AppointmentCancelView(APIView):
  permission_classes = [CanCancel]

  @swagger_auto_schema(request_body=AppointmentCancellationSerializer,
                       responses={200: 'Cancelled'})
  def post(self, request, appointment_id):
    user = request.user
    try:
      appointment = Appointment.objects.get(id=appointment_id)
    except:
      raise APIException('Unauthorized!')

    self.check_object_permissions(self.request, appointment)

    type = request.data.get('type', 'standard')
    AppointmentCancellation.objects.create(appointment=appointment, type=type, user=user)

    appointment.status = 'cancelled'
    appointment.save()

    if user.type == User.PATIENT_TYPE:
      cancellation_time = timezone.now()
      start_time = appointment.start_time
      penalty_time = start_time - timezone.timedelta(hours=24)

      # charge customer 50%
      if cancellation_time > penalty_time:
        amount = int(appointment.price / 2 * 100)
        description = "Moca cancellation fee"
        try:
          stripe_customer_id = PaymentProfile.objects.get(user=user).stripe_customer_id
          charge_customer(stripe_customer_id, amount, description)
        except Exception as e:
          description = f"Cancellation payment of ${amount/100} failed."
          Issue.objects.create(appointment=appointment,
                               therapist=appointment.therapist,
                               patient=appointment.patient,
                               priority="high",
                               description=description)

    return Response("Cancelled", status=status.HTTP_200_OK)


class AppointmentStartView(APIView):
  permission_classes = [CanStart]

  def post(self, request, appointment_id):
    try:
      appointment = Appointment.objects.get(id=appointment_id)
    except:
      raise APIException('Unauthorized!')

    self.check_object_permissions(self.request, appointment)

    appointment.status = 'in-progress'
    appointment.save()

    patient = appointment.patient.user

    # Charge customer
    amount = int(appointment.price * 100)
    description = "Moca appointment"
    payment_failed = False

    try:
      stripe_customer_id = PaymentProfile.objects.get(user=patient).stripe_customer_id
      charge_customer(stripe_customer_id, amount, description)
    except Exception as e:
      appointment.status = 'payment-failed'
      appointment.save()

      description = f"Appointment payment of ${amount/100} failed."
      Issue.objects.create(appointment=appointment,
                           therapist=appointment.therapist,
                           patient=appointment.patient,
                           priority="high",
                           description=description)
      payment_failed = True

    devices = Device.objects.filter(user=patient)

    if payment_failed:
      # Send push notification to patient
      text = f'Payment failed.'

      for device in devices:
        send_push_message(device.token, text, {
          'type': 'failed_payment',
          'params': {
            'user': {
              'id': request.user.id
            }
          }
        })
      return Response("Payment Failed", status=status.HTTP_402_PAYMENT_REQUIRED)

    else:
      text = f'Your appointment with {request.user.first_name} {request.user.last_name} has started.'

      for device in devices:
        send_push_message(device.token, text, {
          'type': 'start_appointment',
          'params': {
            'user': {
              'id': request.user.id
            }
          }
        })

    return Response("Started", status=status.HTTP_200_OK)


class AppointmentEndView(APIView):
  permission_classes = [CanEnd]

  def post(self, request, appointment_id):
    try:
      appointment = Appointment.objects.get(id=appointment_id)
    except:
      raise APIException('Unauthorized!')

    self.check_object_permissions(self.request, appointment)

    appointment.status = 'completed'
    appointment.save()

    devices = Device.objects.filter(user=appointment.patient.user)
    text = f'Your appointment with {request.user.first_name} {request.user.last_name} has ended.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'end_appointment',
        'params': {
          'user': {
            'id': request.user.id
          }
        }
      })

    return Response("Ended", status=status.HTTP_200_OK)
