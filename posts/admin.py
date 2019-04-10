from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'status']
    list_filter = ['published', ]
    date_hierarchy = 'published'
    search_fields = ['title', 'content']
 