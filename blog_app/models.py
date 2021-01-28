from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """
    A Topic is the user is learning about
    """
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    """
    Something Specific learned about a Topic
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]}..."


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return self.author


class Like(models.Model):
    ...
    likes = models.ManyToManyField(User, related_name='like')

    def number_of_likes(self):
        return self.likes.count()
