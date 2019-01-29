from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import Intern
from .forms import *
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    qset = Intern.objects.values().order_by('dateAdded')
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