from django.urls import path
from knox.views import LogoutView

from .views import ReviewListView

urlpatterns = [
  path('<int:therapist_id>/', ReviewListView.as_view())
]
