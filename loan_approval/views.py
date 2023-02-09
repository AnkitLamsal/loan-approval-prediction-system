from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .models import Loan, Applicant
from .forms import LoanModelForm,ApplicantModelForm
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
    if request.POST == 'POST':  
        form = ApplicantModelForm()  
        if form.is_valid():  
            user = form.save()
            Applicant.objects.create(applicant=user)
    else:  
        form = ApplicantModelForm()  
    context = {  
        'form':form  
    }  
    return render(request, 'loan_approval/applicant_registration.html', context)  
    

