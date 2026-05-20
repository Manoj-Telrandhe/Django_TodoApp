from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Task
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'tasks/home.html')
    # return HttpResponse("<h1>Todo App Home page</h1>")
    
    
def register(request):
    
    if request.method == "POST":
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            
            if User.objects.filter(username=username).exists():
                
                messages.error(request, "Username already exists")
                
                return redirect('register')
            
            else:
                User.objects.create_user(username=username, email=email, password=password1)
            
                messages.success(request, "You have registered yourself successfully!")
            
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            
            return redirect('register')
            
    return render(request, 'tasks/register.html')


def login_user(request):
    
    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request,
                            username=username, 
                            password=password
                            )
        
        if user is not None:
            login(request, user)
            
            messages.success(request, "Login Successfully!")
            
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            
            return redirect("login")
            
    return render(request, 'tasks/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out succesfully!')
    return redirect('home')


@login_required
def todos(request):
    
    if request.method == 'POST':
        task_text = request.POST.get("task_text")
        
        Task.objects.create(
            user = request.user,
            task_text = task_text
        )
        
        messages.success(request, "Todo added successfully!")
        
        return redirect('todos')
    
    user_tasks = Task.objects.filter(user=request.user)
    
    context = {
        'tasks' : user_tasks
    }
    
    return render(request, 'tasks/todos.html', context)


@login_required
def delete_task(request, task_id):
    
    task = Task.objects.get(id=task_id, user=request.user)
    
    task.delete()
    
    messages.success(request, "Task deleted successfully!")
    
    return redirect('todos')



@login_required
def toggle_task(request, task_id):
    
    task = Task.objects.get(id=task_id, user=request.user)
    
    task.completed = not task.completed 
    
    task.save()
    
    return redirect('todos')


@login_required
def edit_task(request, task_id):
    
    task = Task.objects.get(id=task_id, user=request.user)
    
    if request.method == "POST":
        updated_text = request.POST.get("task_text")
        
        task.task_text = updated_text
        
        task.save()
        
        messages.success(request, "Task updated successfully!")
        
        return redirect('todos')
    
    context = {
        'task' : task
    }
    
    return render(request, 'tasks/edit_task.html', context)



# Profile
@login_required
def profile(request):

    total_tasks = Task.objects.filter(user=request.user).count()

    completed_tasks = Task.objects.filter(
        user=request.user,
        completed=True
    ).count()

    incomplete_tasks = Task.objects.filter(
        user=request.user,
        completed=False
    ).count()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'incomplete_tasks': incomplete_tasks,
    }

    return render(request, 'tasks/profile.html', context)