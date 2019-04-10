from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'birth', 'image']
    list_filter = ['created', 'updated', 'birth', 'gender']
    date_hierarchy = 'created'
    search_fields = ['user']
