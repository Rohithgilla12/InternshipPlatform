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
# from django.urls import path
from interns.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', home,name="home"),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'},name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^create/$', create, name='create'),
    url(r'interns/(?P<pk>\d{0,50})/$', intern_detail_view, name='intern_detail_view'),
    url(r'interns/(?P<pk>\d+)/edit/$', intern_edit, name='intern_edit'),
    url('students', allStudList, name='allStud'),
    url('profile', myInterns, name='myProfile'),
    url('interns/category/(?P<catName>\w{0,50})/',dispSpecific,name='specific')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# user = User.objects.create_user('16XJ1A0540',password='Test1234')
# user.first_name="Ram"
# user.last_name="Manohar"
# user.email="manohar160540@mechyd.ac.in"
# user.groups.add(students)
# user.profile.leisureTime="Peaks"
# user.profile.location="Student"
# user.save()