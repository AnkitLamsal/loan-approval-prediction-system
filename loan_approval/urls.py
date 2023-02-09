from django.urls import path
from .views import hello_world, applicant_register, employee_register
from .views import ApplicantCreateView

app_name = "credit_risk"
urlpatterns = [
    path('',hello_world,name="index"),
    # path('applicant/',ApplicantCreateView.as_view(),name="applicant_create"),
    path('applicant/register/',applicant_register,name='applicant_register'),
    path('employee/register/',employee_register,name='employee_register'),
]
