from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Loan, LoanDetails, LoanPrediction

class ApplicantModelForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['email','username','password1','password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        return email
    
    def save(self, commit=True):
        user = super(ApplicantForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    
class EmployeeModelForm(UserCreationForm):
    email = forms.EmailField()
    class meta:
        model = User
        fields = ['email','username','password1','password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")
        return email    
    
    def save(self, commit=True):
        user = super(EmployeeForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        user.admin_status = True
        if commit:
            user.save()
        return user
    
    
class LoanModelForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = "__all__"