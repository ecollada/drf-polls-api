"""
Polls application models.
"""

from django.db import models
from django.contrib.auth.models import User


CASCADE = models.CASCADE


class Poll(models.Model):
    """
    Polls model class.
    """
    question = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=CASCADE)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    """
    Choices model class.
    """
    poll = models.ForeignKey(Poll, on_delete=CASCADE)
    text = models.CharField(max_length=144)

    def __str__(self):
        return self.text


class Vote(models.Model):
    """
    Choices' vote model class.
    """
    choice = models.ForeignKey(Choice, on_delete=CASCADE)
    poll = models.ForeignKey(Poll, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)

    class META:
        unique_together = ('poll', 'voted_by',)
