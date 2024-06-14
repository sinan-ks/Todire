from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):

    title = models.CharField(max_length=200)

    options = (
        ('pending','Pending'),
        ('in_progress', 'In Progress'),
        ('completed','Completed'),
    )
    status = models.CharField(max_length=200,choices=options,default='pending')

    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)

    due_date = models.DateTimeField(null=True, blank=True)

    user_object = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


