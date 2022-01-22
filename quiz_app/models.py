"""
    define models for quiz_app
"""

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from authentication.models import User


# Create your models here.

class Quiz(models.Model):
    """a quiz which users can create, like, dislike or add comments"""
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(name="Date Created", auto_now=True)
    likes = models.PositiveIntegerField(name="Likes", default=0)
    dislikes = models.PositiveIntegerField(name="Dislikes", default=0)
    thumbnail = ProcessedImageField(processors=[ResizeToFill(640, 360)], format='WEBP', options={'quality': 60})

    def __str__(self):
        return str(self.title)


class Question(models.Model):
    """
    a single question in a quiz, a quit can have multiple questions
    optionally there can be a time limit for each question
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    time = models.PositiveIntegerField(
        verbose_name="Time to solve the question",
        name="Time",
        null=True
    )


class Option(models.Model):
    """an option which belongs to a question, a question can have multiple options"""
    text = models.CharField(max_length=200)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Comment(models.Model):
    """a comment which users can write and which always belongs to a quiz"""
    text = models.CharField(max_length=1000)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
