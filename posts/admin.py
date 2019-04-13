from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', ]
    list_filter = ['created']
    date_hierarchy = 'created'
    search_fields = ['title', 'content']
 