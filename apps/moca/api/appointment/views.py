from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from moca.api.appointment.serializers import AppointmentSerializer, AppointmentDeserializer, \
  ReviewSerializer, Rating
from moca.api.appointment.errors import AppointmentNotFound, ReviewNotFound
from moca.models.appointment import Appointment, Review


class AppointmentAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, format=None):
    appointment = AppointmentDeserializer(data=request.data)
    appointment.is_valid(raise_exception=True)
    appointment = appointment.save()
    appointment = Appointment.objects.get(id=appointment.id)
    return Response({'appointment': AppointmentSerializer(appointment).data},
                    status.HTTP_201_CREATED)


class AppointmentAPIDetailView(APIView):
  def get(self, request, appointment_id, format=None):
    appointment = Appointment.objects.get(pk=appointment_id)
    appointment = AppointmentSerializer(appointment)
    return Response(appointment.data, status=status.HTTP_200_OK)

  def put(self, request, appointment_id, format=None):
    existing = self.get_appointment(appointment_id)
    # todo check schedule API if new time is available
    appointment = AppointmentSerializer(instance=existing, data=request.data)
    appointment.is_valid(raise_exception=True)
    appointment = appointment.save()
    return Response({"appointment": AppointmentSerializer(appointment).data},
                    status.HTTP_202_ACCEPTED)

  # Used for cancellation
  def delete(self, request, appointment_id, format=None):
    appointment = self.get_appointment(appointment_id)
    appointment.is_cancelled = True
    appointment.save()
    appointment = self.get_appointment(appointment_id)
    return Response({'appointment': AppointmentSerializer(appointment).data},
                    status.HTTP_202_ACCEPTED)

  def get_appointment(self, appointment_id):
    try:
      existing = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
      raise AppointmentNotFound(appointment_id)
    return existing


class ReviewAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, appointment_id, format=None):
    request.data["appointment_id"] = appointment_id
    review = ReviewSerializer(data=request.data)
    review.is_valid(raise_exception=True)
    review = review.save()
    review = Review.objects.get(pk=review.id)
    return Response({"review": ReviewSerializer(review).data}, status.HTTP_201_CREATED)


class ReviewAPIDetailView(APIView):
  def get(self, request, appointment_id, review_id, format=None):
    review = Review.objects.get(pk=review_id)
    review = ReviewSerializer(review)
    return Response(review.data, status=status.HTTP_200_OK)

  def put(self, request, appointment_id, review_id, format=None):
    request.data["appointment_id"] = appointment_id
    existing = self.get_review(review_id)
    review = ReviewSerializer(instance=existing, data=request.data)
    review.is_valid(raise_exception=True)
    review = review.save()
    return Response({'review': ReviewSerializer(review).data}, status.HTTP_202_ACCEPTED)

  def delete(self, request, appointment_id, review_id, format=None):
    review = self.get_review(review_id)
    rating_service = Rating(Rating.Type.DELETE)
    rating_service.calculate(therapist=review.appointment.therapist, old=review.rating)
    review.delete()
    return Response({'result': f'Review with id : {review_id} is deleted'},
                    status.HTTP_202_ACCEPTED)

  def get_review(self, review_id):
    try:
      existing = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
      raise ReviewNotFound(review_id)
    return existing
