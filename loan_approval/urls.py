from django.urls import path
from .views import hello_world, ApplicantCreateView

app_name = "credit_risk"
urlpatterns = [
    path('',hello_world,name="index"),
    path('applicant/',ApplicantCreateView.as_view(),name="applicant_create"),
]
