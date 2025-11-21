from django.db import models

class Task(models.Model):
    """Task model stored in Supabase PostgreSQL"""
    user_email = models.EmailField(max_length=255)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],
        default='medium'
    )
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'core_task'

    def __str__(self):
        return self.title


class Note(models.Model):
    """Note model for simple text storage"""
    user_email = models.EmailField(max_length=255)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        db_table = 'core_note'

    def __str__(self):
        return self.title