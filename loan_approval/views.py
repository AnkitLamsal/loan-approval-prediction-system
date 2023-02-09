from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Loan
from .forms import LoanModelForm
from django.urls import reverse,reverse_lazy

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World");

class ApplicantCreateView(CreateView):
    model = Loan
    form_class = LoanModelForm
    success_url = reverse_lazy('loan_approval:index')
    template_name = 'loan_approval/applicant_create.html'
    

