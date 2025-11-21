from django.contrib import admin
from .models import Task, Note

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_email', 'priority', 'completed', 'due_date', 'created_at')
    list_filter = ('completed', 'priority', 'created_at')
    search_fields = ('title', 'description', 'user_email')
    date_hierarchy = 'created_at'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_email', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'user_email')
    date_hierarchy = 'created_at'