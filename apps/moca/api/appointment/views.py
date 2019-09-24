from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from moca.api.appointment.serializers import AppointmentSerializer, ReviewSerializer, AppointmentDeserializer
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
    existing = get_object_or_404(Appointment, appointment_id)
    appointment = AppointmentSerializer(instance=existing, data=request.data)
    appointment.is_valid(raise_exception=True)
    appointment = appointment.save()
    return Response({AppointmentSerializer(appointment).data}, status.HTTP_202_ACCEPTED)

  # Used for cancellation
  def delete(self, request, appointment_id, format=None):
    appointment = get_object_or_404(appointment_id)
    appointment.set__is_cancelled(True)
    appointment = appointment.save()
    return Response({AppointmentSerializer(appointment).data}, status.HTTP_202_ACCEPTED)


class ReviewAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, appointment_id, format=None):
    request.data.add("appointment", appointment_id)
    review = ReviewSerializer(data=request.data)
    review.is_valid()
    review = review.save()
    return Response({ReviewSerializer(review).data}, status.HTTP_201_CREATED)


class ReviewAPIDetailView(APIView):
  def get(self, request, appointment_id, review_id, format=None):
    review = Review.objects.get(pk=review_id)
    review = ReviewSerializer(review)
    return Response(review.data, status=status.HTTP_200_OK)

  def put(self, request, review_id, format=None):
    existing = get_object_or_404(Review, review_id)
    review = ReviewSerializer(instance=existing, data=request.data)
    review.is_valid(raise_exception=True)
    appointment = review.save()
    return Response({ReviewSerializer(appointment).data}, status.HTTP_202_ACCEPTED)
