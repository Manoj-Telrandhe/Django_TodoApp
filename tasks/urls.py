from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    
    path('login/', views.login_user, name='login'),
    
    path('logout/', views.logout_user, name='logout'),
    
    path('todos/', views.todos, name='todos'),
    
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    
    path('toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    
    path('profile/', views.profile, name='profile'),
]
