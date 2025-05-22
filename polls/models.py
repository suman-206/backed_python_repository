from django.db import models
from django.contrib.auth.models import AbstractUser

class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField("date published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # Changed from 'user_set' to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # Changed to avoid conflict
        blank=True
    )

    def __str__(self):
        return self.username
