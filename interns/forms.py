from django import forms
from .models import Intern
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = Profile
        fields = ('location',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('location',)



class InternForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"Title of the project",
            "class":"input-field"
        }        
    ),label='Title')
    place = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"Place of the Internship",
            "class":"input-field"
        }        
    ),label='Place/ Organisation')
    deadLine = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"Deadline (in words)",
            "class":"input-field"
        }        
    ),label='Deadline')
    duration = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"Number of weeks/months (in detail)",
            "class":"input-field"
        }        
    ),label='Duration')
    eligibility = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':'Student Criteria',
            "class" : "input-field"
        }
    ))
    studentsEnrolled = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"List of students who already enrolled (ignored if None)",
            "class":"input-field"
        }        
    ),label='Students Enrolled')
    studentsApproved = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"List of students who already approved (ignored if None)",
            "class":"input-field"
        }        
    ),label='Students Approved')
    preReq = forms.CharField(widget=forms.TextInput(
        attrs={
            # 'placeholder':"List of pre requisites",
            "class":"input-field autocomplete"
        }               
    ),label='Pre-Requsites')
    description = forms.CharField(widget=forms.Textarea(
        attrs=
        {
            'placeholder':"Description",
            "class":"materialize-textarea"
        }
        ), label='Description')

    stiphend = forms.CharField(widget=forms.TextInput(
        attrs=
        {
            'placeholder':'Stiphend',
            'class':'input-field'
        }
    ))
    class Meta:
        model = Intern
        fields = ("title","preReq","description","place","deadLine","duration","studentsApproved","studentsEnrolled","eligibility","stiphend")
