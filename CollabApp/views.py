from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Project, Task, Note


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# -------------------------------
# Static Pages
# -------------------------------
@login_required
def home_view(request):
    return render(request, 'home.html')

def landing_page(request):
    return render(request, 'landing.html')

@login_required
def myboards_view(request):
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'myboards.html', {'projects': projects})


@login_required
def boardview_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    tasks = project.tasks.all()
    return render(request, 'boardview.html', {
        'project': project,
        'tasks': tasks
    })


@login_required
def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        project = Project.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        return redirect('project_detail', project_id=project.id)
    return render(request, 'create_project.html')

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    tasks = project.tasks.all()
    notes = project.notes.all()
    return render(request, 'project_details.html', {
        'project': project,
        'tasks': tasks,
        'notes': notes
    })


@login_required
def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        Task.objects.create(
            project=project,
            title=title,
            description=description
        )
        return redirect('boardview', project_id=project_id)
    return render(request, 'create_task.html', {'project_id': project_id})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__created_by=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title', '')
        task.description = request.POST.get('description', '')
        task.status = request.POST.get('status', 'pending')
        task.save()
        return redirect('project_detail', project_id=task.project.id)
    return render(request, 'edit_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, project__created_by=request.user)
    project_id = task.project.id
    task.delete()
    return redirect('project_detail', project_id=project_id)


@login_required
def create_note(request, project_id):
    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        Note.objects.create(
            project=project,
            created_by=request.user,
            content=content
        )
        return redirect('project_detail', project_id=project_id)
    return render(request, 'create_note.html', {'project_id': project_id})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, created_by=request.user)
    project_id = note.project.id
    note.delete()
    return redirect('project_detail', project_id=project_id)