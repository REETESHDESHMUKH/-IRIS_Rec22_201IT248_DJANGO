from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class form(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30, default="")
    questions = models.JSONField(null=True, blank=True)

    def __str__(self):
        return (self.title)

class responses(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    form_id = models.ForeignKey(form,on_delete=models.CASCADE)
    responses = models.JSONField(null=True, blank=True)
