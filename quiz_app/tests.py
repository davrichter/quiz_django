"""
    tests for quiz_app
"""

from django.test import TestCase

from . import models


# Create your tests here.

class QuizTestCase(TestCase):
    def setUp(self):
        user = models.User.objects.create(
            username="Test_user",
            password="123"
        )
        models.Quiz.objects.create(
            title="Test Quiz 1",
            user=user,

        )
