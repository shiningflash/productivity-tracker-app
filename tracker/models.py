from django.contrib.auth.models import User
from django.db import models


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_score = models.IntegerField(default=0)
    date = models.DateField()
