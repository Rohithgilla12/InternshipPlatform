"""InternshipPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from interns.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', home,name="home"),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^create/$', create, name='create'),
    path('interns/<int:pk>/', intern_detail_view, name='intern_detail_view'),
    path('interns/<int:pk>/edit/', intern_edit, name='intern_edit'),
    path('students', allStudList, name='allStud'),
    path('profile', myInterns, name='myProfile'),
    path(r'interns/category/<catName>/',dispSpecific,name='specific')
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
