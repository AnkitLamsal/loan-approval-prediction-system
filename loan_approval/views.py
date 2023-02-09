from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Loan, Applicant, Employee
from .forms import LoanRequestModelForm,ApplicantModelForm, EmployeeModelForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Class Based views 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World "+str(request.user));
    
# User Registration
def applicant_register(request): 
    if request.method == "POST":
        user_form = ApplicantModelForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            applicant = user_form.save()
            Applicant.objects.create(applicant= applicant)
            print("applicant created sucessfully.")
            return redirect('loan_approval:index')
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
            return redirect('loan_approval:index')
    elif request.method =="GET":
        user_form = EmployeeModelForm()
    context = {'form':user_form}
    # TODO : change the applicant_registration form after front end submission. 
    return render(request, 'loan_approval/applicant_registration.html',context)
    

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'loan_approval/applicant_registration.html'
    def get_success_url(self):
        return reverse_lazy('loan_approval:index') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('loan_approval:index')


@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanRequestCreateView(CreateView):
    model = Loan
    form_class = LoanRequestModelForm
    success_url = reverse_lazy('loan_approval:index')
    template_name = 'loan_approval/applicant_create.html'
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if(self.request.user.is_staff == False):
            # print(form)
            # print(self.request.user.applicant)
            form.instance.applicant_details = self.request.user.applicant
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return HttpResponse("Admin Cannot Request Loan.")
        
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanRequestListView(ListView):
    model = Loan
    template_name = 'loan_approval/employee_loan_request.html'