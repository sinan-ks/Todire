from django.urls import path
from task import views

urlpatterns = [

    # Task management URLs
    path('tasks/add/', views.TaskCreateView.as_view(), name='task-add'),  # URL for adding a new task
    path('tasks/all/', views.TaskListView.as_view(), name='task-list'),  # URL for listing all tasks
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),  # URL for viewing a specific task's details
    path('tasks/<int:pk>/change/', views.TaskUpdateView.as_view(), name='task-edit'),  # URL for editing a specific task
    path('tasks/<int:pk>/remove/', views.TaskDeleteView.as_view(), name='task-delete'),  # URL for deleting a specific task

    # User authentication URLs
    path('register/', views.SignUpView.as_view(), name='signup'),  # URL for user registration
    path('', views.SignInView.as_view(), name='signin'),  # URL for user sign-in
    path('signout/', views.SignOutView.as_view(), name='signout'),  # URL for user sign-out
    
]
