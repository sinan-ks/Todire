from django.shortcuts import render,redirect
from django.views.generic import View
from task.forms import TaskForm,RegistrationForm,LoginForm
from task.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Count
from django.utils.decorators import method_decorator
from task.decorator import signin_required
from django.contrib import messages
from django.views.decorators.cache import never_cache

decorator = [signin_required, never_cache]
# Create your views here.

#url: localhost:8000/task/tasks/add
#method: get, post

@method_decorator(decorator, name="dispatch")
class TaskCreateView(View):

    def get(self, request, *args, **kwargs):
        form = TaskForm(exclude_status=True)
        return render(request, 'task_add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST, exclude_status=True)
        if form.is_valid():
            form.instance.user_object = request.user
            form.instance.status = 'pending'  # Set default status here
            form.save()
            messages.success(request, "New task has been added successfully")
            return redirect('task-list')
        messages.error(request, "Failed to add task")
        return render(request, 'task_add.html', {'form': form})

    
#url: localhost:8000/task/tasks/all/
#method: get

@method_decorator(decorator, name="dispatch")
class TaskListView(View):

    def get(self, request, *args, **kwargs):
        # Get the status filter from the query parameters
        status_filter = request.GET.get('status')

        # Filter tasks based on the user and status filter
        if status_filter:
            qs = Task.objects.filter(user_object=request.user, status=status_filter)
        else:
            qs = Task.objects.filter(user_object=request.user)

        # Calculate the counts for each status
        pending_count = Task.objects.filter(user_object=request.user, status='pending').count()
        completed_count = Task.objects.filter(user_object=request.user, status='completed').count()
        in_progress_count = Task.objects.filter(user_object=request.user, status='in_progress').count()
        all_count = Task.objects.filter(user_object=request.user).count()

        return render(request, 'task_list.html', {
            'data': qs,
            'pending_count': pending_count,
            'completed_count': completed_count,
            'in_progress_count': in_progress_count,
            'all_count': all_count
        })



#url: localhost:8000/task/tasks/{id}/change/
#method: get, post

@method_decorator(decorator,name="dispatch")   
class TaskUpdateView(View):

    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task_object = Task.objects.get(id=id)
        form = TaskForm(instance=task_object)
        return render(request,'task_edit.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        task_object = Task.objects.get(id=id)
        form = TaskForm(request.POST,instance=task_object)
        if form.is_valid():
            form.save()
            messages.success(request,"Task updated successfully")
            return redirect('task-list')
        messages.error(request,"Failed to change task")
        return render(request,'task_edit.html',{'form':form})

#url: localhost:8000/task/tasks/{id}/
#method: get

@method_decorator(decorator, name='dispatch')    
class TaskDetailView(View):

    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        qs = Task.objects.get(id=id)
        return render(request,"task_detail.html",{"data":qs})

#url: localhost:8000/task/tasks/{id}/remove/
#method: get

@method_decorator(decorator,name="dispatch")
class TaskDeleteView(View):

    def get(self,request,*args,**kwargs):
        id = kwargs.get('pk')
        Task.objects.get(id=id).delete()
        messages.success(request,"Task deleted successfully")
        return redirect('task-list')    
    

#url: localhost:8000/task/register/
#method: get, post
    
class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form = RegistrationForm()
        return render(request,'register.html',{"form":form})
    
    def post(self,request,*args,**kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # User.objects.create_user(**form.cleaned_data)
            form.save()
            messages.success(request,"User account created successfully")
            return redirect("signin")
        messages.error(request,"Failed to create user account!")
        return render(request,'register.html',{"form":form})
    
#url: localhost:8000/task/signin/
#method: get, post
    
class SignInView(View):

    def get(self,request,*args,**kwargs):
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            uname = data.get("username")
            pwd = data.get("password")
            user_object = authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,"User logged-in successfully")
                return redirect('task-list')
        messages.error(request,"Enter a valid username or password!")
        return render(request,'login.html',{'form':form})
    
#url: localhost:8000/task/signout/
#method: get

@method_decorator(decorator,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('signin')
        
    
        