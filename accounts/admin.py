from django.contrib import admin
from .models import GamblerProfile,PasswordChange, GamblerUser
# Register your models here.

class GamblerProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('first_name','last_name','phone_number','sex','date_of_birth')
    list_filter = ('phone_number','date_of_birth')
    list_display = ('first_name','last_name','phone_number','sex','date_of_birth')

class GamblerUserAdmin(admin.ModelAdmin):
    readonly_fields = ('first_name','last_name','phone_number','sex','date_of_birth')
    list_filter = ('phone_number','date_of_birth')
    list_display = ('first_name','last_name','phone_number','sex','date_of_birth')

class PasswordChangeAdmin(admin.ModelAdmin):
    pass

admin.site.register(GamblerProfile, GamblerProfileAdmin)
admin.site.register(GamblerUser, GamblerUserAdmin)
admin.site.register(PasswordChange)