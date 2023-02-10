from django.urls import path
from .views import hello_world, applicant_register, employee_register, logout
from .views import LoanRequestCreateView, UserLoginView, LoanRequestListView, LoanListView
from django.contrib.auth.views import LogoutView

app_name = "loan_approval"
urlpatterns = [
    path('',hello_world,name="index"),
    path('applicant/register/',applicant_register,name='applicant_register'),
    path('employee/register/',employee_register,name='employee_register'),
    # Users related activities.
    path('user/login/',UserLoginView.as_view(),name='user_login'),
    path('user/logout/', LogoutView.as_view(next_page='loan_approval:index'), name='logout'),
    # Loan request related routes
    path('loan/request/',LoanRequestCreateView.as_view(),name="loan_request"),
    path('loan/list/',LoanRequestListView.as_view(), name='employee_loan_list'),
    path('loan/',LoanListView.as_view(), name='applicant_loan_list'),
]
