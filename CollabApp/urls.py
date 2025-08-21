from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.landing_page, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

 
    path('home/', views.home_view, name='home'),
    path('myboards/', views.myboards_view, name='myboards'),

 
    path('project/<int:project_id>/board/', views.boardview_view, name='boardview'),

    # Project Management
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),

    # Task Management
    path('project/<int:project_id>/task/add/', views.create_task, name='create_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    # Note Management
    path('project/<int:project_id>/note/add/', views.create_note, name='create_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]  