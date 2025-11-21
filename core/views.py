from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .supabase_client import get_supabase_client
from .models import Task, Note
import json

def home(request):
    """Home page view"""
    return render(request, 'home.html')

def login_view(request):
    """Login page view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            # Store session in Django session
            request.session['supabase_access_token'] = response.session.access_token
            request.session['supabase_user'] = {
                'id': response.user.id,
                'email': response.user.email
            }
            
            messages.success(request, 'Successfully logged in!')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Login failed: {str(e)}')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def register_view(request):
    """Registration page view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')
        
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'register.html')
    
    return render(request, 'register.html')

def dashboard_view(request):
    """Dashboard view - requires authentication"""
    if 'supabase_access_token' not in request.session:
        messages.warning(request, 'Please login to access the dashboard')
        return redirect('login')
    
    user = request.session.get('supabase_user', {})
    user_email = user.get('email')
    
    # Fetch user's tasks and notes from Supabase PostgreSQL
    tasks = Task.objects.filter(user_email=user_email).order_by('-created_at')
    notes = Note.objects.filter(user_email=user_email).order_by('-created_at')
    
    # Calculate statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    
    context = {
        'user': user,
        'tasks': tasks[:5],  # Show latest 5 tasks
        'notes': notes[:5],  # Show latest 5 notes
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'dashboard.html', context)

def tasks_view(request):
    """Tasks list and create view"""
    if 'supabase_access_token' not in request.session:
        messages.warning(request, 'Please login to access tasks')
        return redirect('login')
    
    user = request.session.get('supabase_user', {})
    user_email = user.get('email')
    
    if request.method == 'POST':
        # Create new task
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date') or None
        
        try:
            Task.objects.create(
                user_email=user_email,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
            messages.success(request, 'Task created successfully!')
            return redirect('tasks')
        except Exception as e:
            messages.error(request, f'Error creating task: {str(e)}')
    
    # Get all user tasks
    tasks = Task.objects.filter(user_email=user_email)
    context = {
        'user': user,
        'tasks': tasks
    }
    return render(request, 'tasks.html', context)

def task_toggle(request, task_id):
    """Toggle task completion status"""
    if 'supabase_access_token' not in request.session:
        return redirect('login')
    
    user_email = request.session.get('supabase_user', {}).get('email')
    task = get_object_or_404(Task, id=task_id, user_email=user_email)
    
    task.completed = not task.completed
    task.save()
    
    status = "completed" if task.completed else "reopened"
    messages.success(request, f'Task {status} successfully!')
    return redirect('tasks')

def task_delete(request, task_id):
    """Delete a task"""
    if 'supabase_access_token' not in request.session:
        return redirect('login')
    
    user_email = request.session.get('supabase_user', {}).get('email')
    task = get_object_or_404(Task, id=task_id, user_email=user_email)
    
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('tasks')

def notes_view(request):
    """Notes list and create view"""
    if 'supabase_access_token' not in request.session:
        messages.warning(request, 'Please login to access notes')
        return redirect('login')
    
    user = request.session.get('supabase_user', {})
    user_email = user.get('email')
    
    if request.method == 'POST':
        # Create new note
        title = request.POST.get('title')
        content = request.POST.get('content', '')
        category = request.POST.get('category', '')
        
        try:
            Note.objects.create(
                user_email=user_email,
                title=title,
                content=content,
                category=category
            )
            messages.success(request, 'Note created successfully!')
            return redirect('notes')
        except Exception as e:
            messages.error(request, f'Error creating note: {str(e)}')
    
    # Get all user notes
    notes = Note.objects.filter(user_email=user_email)
    context = {
        'user': user,
        'notes': notes
    }
    return render(request, 'notes.html', context)

def note_delete(request, note_id):
    """Delete a note"""
    if 'supabase_access_token' not in request.session:
        return redirect('login')
    
    user_email = request.session.get('supabase_user', {}).get('email')
    note = get_object_or_404(Note, id=note_id, user_email=user_email)
    
    note.delete()
    messages.success(request, 'Note deleted successfully!')
    return redirect('notes')

def logout_view(request):
    """Logout view"""
    try:
        if 'supabase_access_token' in request.session:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
        
        # Clear Django session
        request.session.flush()
        messages.success(request, 'Successfully logged out!')
    except Exception as e:
        messages.error(request, f'Logout error: {str(e)}')
    
    return redirect('home')