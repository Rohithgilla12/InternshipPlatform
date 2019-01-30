from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Intern
from .forms import *
from django.contrib.auth.models import User
from .temp import *

studentMap = {
    "16XJ1A0515":"Rohith Gilla",
    "16XJ1A504":"Abhinav Reddy",
    "16XJ1A503":"Abhimanyu Bellam",
    "16XJ1A0210":"Vishal Reddy",
}

# Create your views here.

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
    print(request.user.is_authenticated)
    pk=kwargs['pk']
    obj = Intern.objects.get(id=pk)  # GET from database
    print(obj)
    tempUser = (User.objects.filter(id=obj.user_id))
    context = {
        "object": obj,
        "user":tempUser[0]
    }
    return render(request, "detail_view.html", context)



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
