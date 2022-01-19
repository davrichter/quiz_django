from django.db import models

from authentication.models import User


# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(name="Likes")
    dislikes = models.PositiveIntegerField(name="Dislikes")
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    time = models.PositiveIntegerField(verbose_name="Time to solve the question", name="Time")


class Option(models.Model):
    text = models.CharField(max_length=200)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
