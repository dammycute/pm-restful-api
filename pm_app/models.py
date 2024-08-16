from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    project_type = models.CharField(max_length=50, blank=True)
    employer_name = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects', blank=True, null=True)
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title
