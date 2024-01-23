from django.contrib import admin

# Register your models here.
from .models import UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ["id","name", "username", "job_num", "last_login", "role", "date_joined"]


admin.site.register(UserProfile, UserAdmin)
