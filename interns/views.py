from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Intern
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import re
from .temp import *

# Create your views here.

rolMatch=re.compile(r'[15,16,17,18]+[XJ,xj,Xj,xJ]+1A0[1-3,5][0-9][0-9]')

def group_required(*group_names):
   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups,login_url='/')



def home(request):
    qset = Intern.objects.values().order_by('-dateAdded')
    for obj in qset:
        tempUser = (User.objects.filter(id=obj['user_id']))[0]
        fulName = tempUser.first_name + " "+tempUser.last_name
        obj.update({
            "fullName":fulName
        })
    print(qset)
    return render(request, 'home.html',{'qset':qset})

@login_required
@group_required("Professor")
def create(request):
    if request.method == "POST":
        form = InternForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user            
            post.save()
            return redirect('home')
    else:
        form = InternForm()        
    return render(request,'create.html',{'form':form})


def intern_detail_view(request, *args,**kwargs):
    print("Came") 
    pk=kwargs['pk']
    message=""
    obj = Intern.objects.get(id=pk)  # GET from database  
    allInterns = Intern.objects.all()
    userNumber = str(request.user.username)
    internsApplied=[]
    if request.method == 'POST':
        if "apply" in request.POST:
            if (str(request.user.username) not in obj.studentsEnrolled):
                try:
                    if obj.studentsEnrolled[-1]!=',':
                        obj.studentsEnrolled+=','
                except:
                    pass
                try:
                    obj.studentsEnrolled+=str(request.user.username)+","
                except:
                    obj.studentsEnrolled = str(request.user.username)
                obj.save()
                message='Done!'        
            else:
                message='Repeated'
            for intern in allInterns:
                if(userNumber in intern.studentsEnrolled): 
                    internsApplied.append(intern.title)
        if "approve" in request.POST:
            approvedRoll = request.POST['studentRoll']
            approvedRoll = approvedRoll.upper()
            if rolMatch.match(approvedRoll):
                obj.studentsApproved +=str(approvedRoll)+','
                print(approvedRoll,obj.studentsEnrolled, approvedRoll in obj.studentsEnrolled)
                if approvedRoll in obj.studentsEnrolled:
                    obj.studentsEnrolled=obj.studentsEnrolled.replace(approvedRoll+',','')
                obj.save()
                message='Student had been approved successfully'
            else:
                message="Roll Number is invalid or format is invalid"
        
        if "disapprove" in request.POST:
            disApprovedRoll = request.POST['studentRoll']
            disApprovedRoll= disApprovedRoll.upper()
            if rolMatch.match(disApprovedRoll):
                if disApprovedRoll in obj.studentsApproved:
                    obj.studentsApproved = obj.studentsApproved.replace(disApprovedRoll+',','')
                    message = "Student has been disapproved successfully"
                else:
                    message="Roll Number is invalid or format is invalid"
    
    enrolledKids=obj.studentsEnrolled.split(',')
    enrollmentString=''
    for kid in enrolledKids[:-1]:
        myInters=Intern.objects.filter(studentsEnrolled__contains=kid)
        enrollmentString+=kid+"("+str(len(myInters))+"),"
    tempUser = (User.objects.filter(id=obj.user_id))
    context = {
        "object": obj,
        "user":tempUser[0],
        "message":message,
        "appliedInterns":','.join(internsApplied),
        "enrollmentString":enrollmentString
    }
    return render(request, "detail_view.html", context)


@login_required
def intern_edit(request, pk):
    inter = get_object_or_404(Intern, pk=pk)       
    if(request.user.id == inter.user_id):
        if request.method == "POST":
            form = InternForm(request.POST, instance=inter)
            if form.is_valid():
                inter = form.save(commit=False)
                inter.user = request.user
                inter.save()
                return redirect('intern_detail_view', pk=inter.id)
        else:
            form = InternForm(instance=inter)
        return render(request, 'edit.html', {'form': form})
    else:
        return render(request,'forbidden.html',{})

@login_required
def allStudList(request):
    CseStudents=User.objects.filter(username__contains="16XJ1A05")
    EeeStudents=User.objects.filter(username__contains="16XJ1A02")
    MechStudents=User.objects.filter(username__contains="16XJ1A03")
    CivilStudents=User.objects.filter(username__contains="16XJ1A01")
    for kid in CseStudents:
        kidInterns = Intern.objects.filter(studentsEnrolled__contains=kid.username)
        kidSelected=Intern.objects.filter(studentsApproved__contains=kid.username)
        for eachIntern in kidInterns:
            if kid.profile.enrolledInternships is None:
                kid.profile.enrolledInternships = eachIntern.title+','
            else:
                kid.profile.enrolledInternships += eachIntern.title+','
        for eachIntern in kidSelected:
            if kid.profile.acceptedInternships is None:
                kid.profile.acceptedInternships = eachIntern.title+','
            else:
                kid.profile.acceptedInternships += eachIntern.title+','
    for kid in MechStudents:
        kidInterns = Intern.objects.filter(studentsEnrolled__contains=kid.username)
        kidSelected=Intern.objects.filter(studentsApproved__contains=kid.username)
        for eachIntern in kidInterns:
            if kid.profile.enrolledInternships is None:
                kid.profile.enrolledInternships = eachIntern.title+','
            else:
                kid.profile.enrolledInternships += eachIntern.title+','
        for eachIntern in kidSelected:
            if kid.profile.acceptedInternships is None:
                kid.profile.acceptedInternships = eachIntern.title+','
            else:
                kid.profile.acceptedInternships += eachIntern.title+','
    for kid in EeeStudents:
        kidInterns = Intern.objects.filter(studentsEnrolled__contains=kid.username)
        kidSelected=Intern.objects.filter(studentsApproved__contains=kid.username)
        for eachIntern in kidInterns:
            if kid.profile.enrolledInternships is None:
                kid.profile.enrolledInternships = eachIntern.title+','
            else:
                kid.profile.enrolledInternships += eachIntern.title+','
        for eachIntern in kidSelected:
            if kid.profile.acceptedInternships is None:
                kid.profile.acceptedInternships = eachIntern.title+','
            else:
                kid.profile.acceptedInternships += eachIntern.title+','
    for kid in CivilStudents:
        kidInterns = Intern.objects.filter(studentsEnrolled__contains=kid.username)
        kidSelected=Intern.objects.filter(studentsApproved__contains=kid.username)
        for eachIntern in kidInterns:
            if kid.profile.enrolledInternships is None:
                kid.profile.enrolledInternships = eachIntern.title+','
            else:
                kid.profile.enrolledInternships += eachIntern.title+','
        for eachIntern in kidSelected:
            if kid.profile.acceptedInternships is None:
                kid.profile.acceptedInternships = eachIntern.title+','
            else:
                kid.profile.acceptedInternships += eachIntern.title+','
    context = {
        "CSE":CseStudents,
        "MECH":MechStudents,
        "EEE":EeeStudents,
        "CIVIL":CivilStudents
    }
    return render(request,'studlist.html',context)

@login_required
def myInterns(request):    
    pk=request.user.id
    if "XJ1A" in str(request.user.username):        
        myInters=Intern.objects.filter(studentsEnrolled__contains=request.user.username)
        approvedInterns = Intern.objects.filter(studentsApproved__contains=request.user.username)
    else:
        myInters=Intern.objects.all().filter(user_id=pk)
        approvedInterns=""
    tempUser = (User.objects.filter(id=pk))[0]
    fulName = tempUser.first_name + " "+tempUser.last_name
    if(request.method=="POST"):
        if "location" in request.POST:
            # location=request.POST['details']        
            location=request.POST['details']
            # print(request.POST['details'])
            if location is None or location =='':
                pass
            else:
                tempUser.profile.location=location
        
        if "time" in request.POST:
            location=request.POST['timeDetail']                  
            if location is None or location =='':
                pass
            else:
                tempUser.profile.leisureTime= location        
        tempUser.save()
    context={
        "qset":myInters,
        "approvedInters":approvedInterns
    }
    return render(request,'profile.html',context)

def dispSpecific(request,*args,**kwargs):
    catName=kwargs["catName"]
    if catName=="all":
        objects=Intern.objects.all()
    else:
        objects=Intern.objects.all().filter(discipline=catName)
    context={
        "obj":objects
    }
    return render(request,'specific.html',context)


# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from interns.models import User
# new_group, created = Group.objects.get_or_create(name ='stu_prof')
# ct = ContentType.objects.get_for_model(User)
# permission = Permission.objects.create(codename ='student', name ='Student', content_type = ct)
# new_group.permissions.add(permission)
# permission = Permission.objects.create(codename ='professor', name ='Professor', content_type = ct)
# new_group.permissions.add(permission)


# from django.contrib.auth.models import Group
# from django.contrib.auth.models import User
# user = User.objects.create_user('16XJ1A0540',password='Test1234')
# user.first_name="Ram"
# user.last_name="Manohar"
# user.email="manohar160540@mechyd.ac.in"
# user.groups.add(students)
# user.profile.leisureTime="Peaks"
# user.profile.location="Student"
# user.save()