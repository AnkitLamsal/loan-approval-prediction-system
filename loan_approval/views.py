from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Loan, Applicant, Employee
from .forms import LoanModelForm,ApplicantModelForm, EmployeeModelForm
from django.urls import reverse,reverse_lazy

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World");

class ApplicantCreateView(CreateView):
    model = Loan
    form_class = LoanModelForm
    success_url = reverse_lazy('loan_approval:index')
    template_name = 'loan_approval/applicant_create.html'
    
    # User Registration
def applicant_register(request): 
    if request.method == "POST":
        user_form = ApplicantModelForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            applicant = user_form.save()
            Applicant.objects.create(applicant= applicant)
            print("applicant created sucessfully.")
            return redirect('credit_risk:index')
    elif request.method =="GET":
        user_form = ApplicantModelForm()
    context = {'form':user_form}
    return render(request, 'loan_approval/applicant_registration.html',context)

def employee_register(request): 
    if request.method == "POST":
        user_form = EmployeeModelForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            employee = user_form.save()
            Employee.objects.create(employee=employee)
            print("applicant created sucessfully.")
            return redirect('credit_risk:index')
    elif request.method =="GET":
        user_form = EmployeeModelForm()
    context = {'form':user_form}
    # TODO : change the applicant_registration form after front end submission. 
    return render(request, 'loan_approval/applicant_registration.html',context)
    

