from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse  
from .models import Loan, Applicant, Employee, LoanDetails, LoanPrediction
from .forms import LoanRequestModelForm,ApplicantModelForm, EmployeeModelForm, LoanDetailsModelForm
from django.urls import reverse,reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Class Based views 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from .utils import Model
from .populate_database import Loader

# Create your views here.
# def hello_world(request):
#     return HttpResponse("Hello World "+str(request.user));

def index(request):
    l = Loader()
    l.load_csv()
    # l.split_columns()
    return render(request, 'loan_approval/index.html',{})

def dashboard(request):
    return render(request, 'loan_approval/dashboard.html',{})

def about(request):
    return render(request, 'loan_approval/about.html',{})

def contact(request):
    return render(request, 'loan_approval/contact.html',{})

def working(request):
    return render(request, 'loan_approval/howitworks.html',{})

# def apply_now(request):
#     return render(request, 'loan_approval/about.html',{})
# User Registration
def applicant_register(request): 
    if request.method == "POST":
        user_form = ApplicantModelForm(request.POST)
        if user_form.is_valid():
            print(user_form.cleaned_data)
            applicant = user_form.save()
            Applicant.objects.create(applicant= applicant)
            print("applicant created sucessfully.")
            return redirect('loan_approval:user_login')
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
            return redirect('loan_approval:user_login')
    elif request.method =="GET":
        user_form = EmployeeModelForm()
    context = {'form':user_form}
    # TODO : change the applicant_registration form after front end submission. 
    return render(request, 'loan_approval/employee_registration.html',context)
    

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'loan_approval/login.html'
    def get_success_url(self):
        return reverse_lazy('loan_approval:dashboard') 
    

@login_required
def logout_view(request):
    logout(request)
    return redirect('loan_approval:index')

@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanRequestCreateView(CreateView):
    model = Loan
    form_class = LoanRequestModelForm
    success_url = reverse_lazy('loan_approval:applicant_loan_list')
    template_name = 'loan_approval/applicant_loan_request_form.html'
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            form.instance.applicant_details = self.request.user.applicant
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanRequestListView(ListView):
    model = Loan
    template_name = 'loan_approval/applicant_loan_request.html'
    
    def get_queryset(self):
        queryset = self.model._default_manager.all()
        try:
            user = self.request.user.applicant
        except:
            return queryset
        else:
            return queryset.filter(applicant_details = user)
    
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanListView(ListView):
    model = Loan
    template_name = 'loan_approval/employee_loan_request.html'
    
    def get_queryset(self):
        queryset = self.model._default_manager.all()
        try:
            user = self.request.user.employee
        except:
            return queryset
        else:
            return queryset.filter(managed_by = user)

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def loanDetailsCreateView(request,pk):
    context = {}
    queryset = Loan.objects.get(id=pk)
    if request.method == "GET":
        context['home_ownership'] = queryset.home_ownership
        context['emp_length'] = queryset.emp_length
        context['loan_amount'] = queryset.loan_amount
        context['person_age'] = queryset.person_age
        context['income'] = queryset.income
        context['loan_intent'] = queryset.loan_intent
        context['id'] = pk
        # print(queryset.managed_by, queryset.applicant_details)
        form = LoanDetailsModelForm()
        context['form'] = form
        return render(request, 'loan_approval/loan_details_form.html',context)
    elif request.method == "POST":
        print("POST")
        id = pk
        # print(id)
        form = LoanDetailsModelForm(request.POST)
        context['home_ownership'] = queryset.home_ownership
        context['emp_length'] = queryset.emp_length
        context['loan_amount'] = queryset.loan_amount
        context['person_age'] = queryset.person_age
        context['income'] = queryset.income
        context['loan_intent'] = queryset.loan_intent
        context['id'] = pk
        context['form'] = form
        if form.is_valid():
            loan_details = form.save(commit=False)
            # print(form.cleaned_data)
            loan_details.loan_request = queryset
            loan_details.save()
            model = create_model(queryset)
            loan_status = model.predict_data()
            prediction = LoanPrediction.objects.create(loan_data=queryset, loan_status=loan_status, prediction_status=True)
            print(prediction)
            prediction.save()
        else:
            return render(request, 'loan_approval/loan_details_form.html',context)
        return redirect('loan_approval:index')
    
@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanDetailsListView(ListView):
    model = LoanDetails
    template_name = 'loan_approval/loan_details_list.html'
    
    def get_queryset(self):
        queryset = self.model._default_manager
        try:
            user = self.request.user.employee
        except:
            print("User is applicant.")
        else:
            # loan = LoanDetails.objects.filter(loan_request__managed_by = employee)
            return queryset.filter(loan_request__managed_by = user)
        try:
            user = self.request.user.applicant
            # print("Applicant view")
        except:
            print("User is employee.")
        else:
            # loan = LoanDetails.objects.filter(loan_request__managed_by = employee)
            return queryset.filter(loan_request__applicant_details = user)

@method_decorator(login_required(login_url=reverse_lazy('loan_approval:user_login')),name="dispatch")
class LoanDetailsDetailView(DetailView):
    model = LoanDetails
    template_name = 'loan_approval/detailed_loan_details_.html'

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def update_loan_request(request,id):
    if request.method =="GET":
        obj = get_object_or_404(Loan, id=id)
        form = LoanRequestModelForm(request.GET or None, instance = obj)
        return render(request, 'loan_approval/loan_update.html',{"form":form})
    elif request.method =="POST":
        # loan = Loan.objects.get(id = id)
        loan_details = LoanDetails.objects.filter(loan_request__id = id)
        if loan_details:
            print(loan_details)
            loan_details.delete()
            print("Object deleted.")
        obj = get_object_or_404(Loan, id=id)
        form = LoanRequestModelForm(request.POST or None, instance = obj)
        if form.is_valid():
            print(form)
            form.save()
        else:
            return render(request, 'loan_approval/loan_update.html',{"form":form})
        return redirect("loan_approval:applicant_loan_list")

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def delete_loan(request,id):
    # fetch the object related to passed id
    if request.user.is_authenticated:
        condition1 = request.user.is_staff
        condition2 = request.user.is_superuser
        print(condition1, condition2)
        if not (condition1 or condition2):
            obj = get_object_or_404(Loan, id = id)
            # delete object
            obj.delete()
            # after deleting redirect to home page.
            return redirect("loan_approval:applicant_loan_list")
        else:
            return HttpResponse("<h3> SuperAdmin or Employee cannot delete loan request. </h3>")

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def update_loan_details(request,pk):
    context = {}
    obj = get_object_or_404(LoanDetails, id = pk)
    context['home_ownership'] = obj.loan_request.home_ownership
    context['emp_length'] = obj.loan_request.emp_length
    context['loan_amount'] = obj.loan_request.loan_amount
    context['person_age'] = obj.loan_request.person_age
    context['income'] = obj.loan_request.income
    context['loan_intent'] = obj.loan_request.loan_intent
    if request.method == "GET":        
        form = LoanDetailsModelForm(request.GET or None, instance = obj)
        # form = LoanDetailsModelForm()
        context['form'] = form
        return render(request, 'loan_approval/loan_details_form.html',context)
    elif request.method == "POST":
        form = LoanDetailsModelForm(request.POST or None, instance = obj)
        context['form'] = form
        if form.is_valid():
            print("Form is valid.")
            # print(form)
            form.save()
            return redirect("loan_approval:applicant_loan_list")
        else:
            return render(request, 'loan_approval/loan_details_form.html',context)

@login_required(login_url=reverse_lazy('loan_approval:user_login'))
def predict(request,pk):
    # print(not request.user.is_superuser)
    condition1 = request.user.is_superuser
    condition2 = request.user.is_authenticated
    # print(condition1 and condition2 )
    if  condition2:
    # Function used by machine learning.
        if condition1:
            context = {}
            context['error'] = "403: Super user cannot look after loan approval prediction."
            return JsonResponse(context, status=403)
        else:
            obj = get_object_or_404(Loan, id = pk)
            model = create_model(obj)
            loan_status = model.predict_data()
            # Pipelining and others.
        # print(obj.loanprediction)
            prediction_status = True
            prediction_object = obj.loanprediction
            # print(prediction_object)
            prediction_object.prediction_status = prediction_status
            prediction_object.loan_status = loan_status
            prediction_object.save()
            print(prediction_object, prediction_object.loan_status, prediction_object.prediction_status)
            # prediction_object.objects.update(prediction_status = True, loan_status= loan_status)    
            context = {}
            context['prediction']  = loan_status
            # print(context)
            return JsonResponse(context, status=200)
    else:
        context = {}
        context['error'] = "404:  cannot view loan approval prediction."
        return JsonResponse(context, status=404)
        

def create_model(loan):
    person_age = loan.person_age
    income = loan.income
    intent = loan.loan_intent
    emp_length = loan.emp_length
    amount = loan.loan_amount
    ownership = loan.home_ownership
    credit_history = loan.loandetails.credit_history
    rate = loan.loandetails.interest_rate
    default = loan.loandetails.credit_default
    grade = loan.loandetails.grade
    percent_to_income = loan.loandetails.loan_percent_to_income
    print(person_age)
    model = Model(
        person_age = person_age,
        person_income = income,
        home_ownership = ownership,
        employment_length = emp_length,
        intent = intent,
        grade = grade,
        amount = amount,
        interest_rate = rate,
        percent_to_income = percent_to_income,
        default_on_file = default,
        credit_history_length = credit_history
    )
    return model
