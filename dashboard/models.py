from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.title

class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Subject=models.CharField(max_length=20)
    title=models.CharField(max_length=30)
    description=models.TextField()
    due_date=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title
