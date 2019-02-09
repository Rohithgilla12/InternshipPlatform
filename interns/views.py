from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Intern
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .temp import *

# Create your views here.


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
    pk=kwargs['pk']
    message=""
    obj = Intern.objects.get(id=pk)  # GET from database  
    allInterns = Intern.objects.all()
    userNumber = str(request.user.username)
    internsApplied=[]
    if request.method == 'POST':
        if (str(request.user.username) not in obj.studentsEnrolled):
            obj.studentsEnrolled+=str(request.user.username)+","
            obj.save()
            message='Done!'        
        else:
            message='Repeated'
        for intern in allInterns:
            if(userNumber in intern.studentsEnrolled):
                internsApplied.append(intern.title)

    tempUser = (User.objects.filter(id=obj.user_id))
    context = {
        "object": obj,
        "user":tempUser[0],
        "message":message,
        "appliedInterns":','.join(internsApplied)
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
    studentsEnrolled= Intern.objects.all().values('id','title','studentsEnrolled')
    studentsApproved= Intern.objects.all().values('id','title','studentsApproved')      
    for obj in studentsEnrolled:
        reqString = obj['studentsEnrolled']        
        reqList = reqString.split(',')
        names=''
        branches=''
        years=''
        print(reqList)
        for name in reqList:
            try:            
                names+=search2(name)[0]+', '
                branches+=search2(name)[2]+', '
                years+=search2(name)[1]+', '
            except:
                pass
        print(names)
        obj.update({
            "retrivedName":names[:-2],
            "branches": branches[:-2],
            "years":years[:-2]
        })

    for obj in studentsApproved:
        reqString = obj['studentsApproved']
        reqList = reqString.split(',')
        names=''
        years=''
        branches=''
        for name in reqList:            
            try:            
                years+=search2(name)[1]+', '
                names+=search2(name)[0]+', '
                branches+=search2(name)[2]+', '
                # years+=search2(name)[1]+', '
                
            except:
                pass        
        obj.update({
            "retrivedName":names[:-2],
            "branches": branches[:-2],
            "years":years[:-2]
        })
    context = {
        "studentsEnrolled":studentsEnrolled,
        "studentsApproved":studentsApproved
    }
    return render(request,'studlist.html',context)

@login_required
def myInterns(request):
    pk=request.user.id
    myInters=Intern.objects.all().filter(user_id=pk)
    tempUser = (User.objects.filter(id=pk))[0]
    fulName = tempUser.first_name + " "+tempUser.last_name
    context={
        "qset":myInters
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
# user = User.objects.create_user('foo',password='bar')
# user.first_name="Fucked up"
# user.last_name="Beyond Login"
# user.email="foobar@gilmail.com"
# user.groups.add(students)
# user.profile.leisureTime="Peaks"
# user.profile.location="Facult office"
# user.save()