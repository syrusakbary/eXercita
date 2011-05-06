from django.db import models
from picklefield.fields import PickledObjectField
DOCUMENT_STATES = (
    ('OK', 'OK'),
    ('ER', 'Error'),
    ('PR', 'Processing'),
)
IMAGE_SIZE = {
    'big': (580,816),
    'small': (220,308),
}

import os
from settings import EXERCITA
class Document(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    content = models.TextField()
    data = PickledObjectField()
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    author = models.ForeignKey('auth.User')
    public = models.BooleanField()
    state = models.CharField(max_length=2, choices=DOCUMENT_STATES)
    pages = models.SmallIntegerField(default=1)
    def image (self,i,size):
        if type(size)==str:
            size = IMAGE_SIZE[size]
        return self.file('thumbnail_%s_%d_%d.png'%(i,size[0],size[1]))
        
    def pdf (self):
        return self.file('document.pdf')
    
    def base (self):
        return os.path.join(EXERCITA['DOCUMENTS'],str(self.pk))

    def file(self,name):
        return os.path.join(EXERCITA['DOCUMENTS'],str(self.pk),name)
        
    def latex (self):
        from django.template.loader import render_to_string
        return render_to_string('documents/document_detail.tex', {'data':self.data,'exercises':self.exercises()})

    def exercises (self):
        from exercises.models import Exercise
        if type(self.data) != dict: self.data = {}
        e = self.data.get('exercises','')
        e = e.split(';')
        import re
        pattern = re.compile('(\d+)\[?([^\]]*)\]?')
        exercises = []
        for exercise in e:
            try:
                matches = pattern.match(exercise)
                id = int(matches.group(1))
                sections = matches.group(2).split(',')
                model = Exercise.objects.get(id=id)
                exercises.append({'sections':model.sections(),'path':model.path,'title':unicode(model.title),'id':model.id,'checked':sections})
            except:
                pass
                
        return exercises


    def save (self,create_related=True):
        self.state = 'PR'
        super(Document, self).save()
        if create_related:
            from tasks import CreateRelated
            thread = CreateRelated(self)
            thread.start()