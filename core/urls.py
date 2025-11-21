from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    # Tasks
    path('tasks/', views.tasks_view, name='tasks'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle, name='task_toggle'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    
    # Notes
    path('notes/', views.notes_view, name='notes'),
    path('notes/<int:note_id>/delete/', views.note_delete, name='note_delete'),
]