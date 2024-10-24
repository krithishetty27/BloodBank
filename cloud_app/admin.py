from django.contrib import admin
from .models import Appointment,Test
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Test)
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','status']
    fields = ('user',  'file_upload','status')  # Add report field here

admin.site.register(UserProfile, UserProfileAdmin)