from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):

    # data
    title = models.CharField(max_length=255)
    description = models.TextField()
    voters = models.ManyToManyField(User, blank=True)
    votes = models.PositiveIntegerField(default=0)

    # meta 
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # relational
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True, related_name='created_ideas')
    app = models.ForeignKey('App', on_delete=models.CASCADE, blank=True, null=True, related_name='ideas')

    def __str__(self):
        return f'App:{self.app} - Title:{self.title}'
    
    class Meta():
        ordering = ['-votes']

    def update_votes(self):
        self.votes = self.voters.count()


class App(models.Model):

    # data
    title = models.CharField(max_length=255)
    description = models.TextField()

    # meta
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # relational
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True)


    def __str__(self):
        return self.title
    
    class Meta():
        ordering = ['title']
