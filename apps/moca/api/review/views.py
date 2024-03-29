from rest_framework import generics

from .serializers import ReviewSerializer
from moca.models.appointment import Review


class ReviewListView(generics.ListAPIView):
  serializer_class = ReviewSerializer

  def get_queryset(self):
    therapist_id = self.kwargs['therapist_id']

    reviews = Review.objects.filter(therapist_id=therapist_id)
    return reviews
