from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True, related_name='created_ideas')
    voters = models.ManyToManyField(User, blank=True)
    votes = models.PositiveIntegerField(default=0)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta():
        ordering = ['-votes']

    def update_votes(self):
        self.votes = self.voters.count()

