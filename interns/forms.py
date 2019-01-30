from django import forms
from .models import Intern
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

INTERN_CHOICES= [
    ('CSE', 'CSE'),
    ('EEE', 'EEE'),
    ('CIVIL', 'CIVIL'),
    ('MECH', 'MECH'),
    ('Management', 'Management'),
    ('Humanities', 'Humanities'),
    ('Media', 'Media'),
    ('Finance', 'Finance')
    ]

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
    discipline=forms.ChoiceField(choices = INTERN_CHOICES, label="Discipline", initial='', widget=forms.Select(
        attrs={
            "class":"dropdown-button btn-flat",
            "style":"color:black"
        }
    ), required=True)
                
    place = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"Place of the Internship",
            "class":"input-field"
        }        
    ),label='Place/ Organisation')
    deadLine = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"Deadline",
            "class":"datepicker"
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
    ),label='Students Enrolled',required=False)
    studentsApproved = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder':"List of students who already approved (ignored if None)",
            "class":"input-field"
        }        
    ),label='Students Approved',required=False)
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
            "class":"materialize-textarea",
            'id':"textarea1"
        }
        ), label='Description')

    stiphend = forms.CharField(widget=forms.TextInput(
        attrs=
        {
            'placeholder':'Stipend',
            'class':'input-field'
        }
    ))
    class Meta:
        model = Intern
        fields = ("title","discipline","preReq","description","place","deadLine","duration","studentsApproved","studentsEnrolled","eligibility","stiphend")
