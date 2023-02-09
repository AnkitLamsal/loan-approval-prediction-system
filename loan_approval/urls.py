from django.urls import path
from .views import hello_world, applicant_register, employee_register, logout
from .views import LoanRequestCreateView, UserLoginView
from django.contrib.auth.views import LogoutView

app_name = "loan_approval"
urlpatterns = [
    path('',hello_world,name="index"),
    path('loan/request/',LoanRequestCreateView.as_view(),name="loan_request"),
    path('applicant/register/',applicant_register,name='applicant_register'),
    path('employee/register/',employee_register,name='employee_register'),
    path('user/login/',UserLoginView.as_view(),name='user_login'),
    path('user/logout/', LogoutView.as_view(next_page='loan_approval:index'), name='logout'),
]
