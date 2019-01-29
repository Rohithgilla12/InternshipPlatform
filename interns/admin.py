from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# from .models import Note
from .models import Intern
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    # list_display = ('username', 'email', 'first_name', 'last_name')
    list_select_related = ('profile', )

    # def get_dist(self, instance):
    #     return instance.profile.dist_code
    # get_dist.short_description = 'Dist Code'

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(CustomUserAdmin, self).get_inline_instances(request, obj)





# Register your models here.

admin.site.register(Profile)
admin.site.register(Intern)

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)