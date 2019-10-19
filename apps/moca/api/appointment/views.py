from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from moca.api.appointment.serializers import AppointmentSerializer, \
  ReviewSerializer, Rating, AppointmentCreateUpdateSerializer
from moca.api.appointment.errors import AppointmentNotFound, ReviewNotFound
from moca.models.appointment import Appointment, Review


class AppointmentListCreateView(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated]

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AppointmentCreateUpdateSerializer
    else:
      return AppointmentSerializer

  def get_queryset(self):
    user = self.request.user
    user_profile_model = user.get_profile_model()
    user_profile_type = user.get_profile_type()
    user_profile = user_profile_model.objects.get(user=user)
    filter_dict = {user_profile_type: user_profile}
    return Appointment.objects.filter(**filter_dict)


class AppointmentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'appointment_id'
  queryset = Appointment.objects.all()

  def get_serializer_class(self):
    if self.request.method == 'GET':
      return AppointmentSerializer
    else:
      return AppointmentCreateUpdateSerializer

 
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
