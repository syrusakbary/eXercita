from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    body = models.TextField()
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    author = models.ForeignKey('auth.User')
    public = models.BooleanField()
    
class Exercise(models.Model):
    path = models.CharField(max_length=200)
    body = models.TextField()