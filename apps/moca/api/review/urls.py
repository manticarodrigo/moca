from django.urls import path

from .views import ReviewListView

urlpatterns = [
  path('<int:therapist_id>/', ReviewListView.as_view())
]
