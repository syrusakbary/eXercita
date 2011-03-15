from django.db import models
from picklefield.fields import PickledObjectField
import re

class Document(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField()
    data = PickledObjectField()
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    #author = models.ForeignKey('auth.User')
    public = models.BooleanField()
    
class Exercise(models.Model):
    path = models.CharField(max_length=255,unique=True)
    content = models.TextField()
    title = models.TextField()
    description = models.TextField()
    
    _pattern = re.compile(r"\\exer{(?P<section>example|part|hint|solution)}{(?P<name>\w+)}",re.DOTALL | re.MULTILINE)
    def sections (self):
        r = {}
        for section,name in self._pattern.findall(self.content):
            a = r.get(section,set())
            a.add(name)
            r[section] = a
        for s in r.keys():
            r[s] = list(r[s])
        return r