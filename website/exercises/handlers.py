from piston.handler import BaseHandler
from piston.utils import rc, throttle
from models import Exercise

class ExercisesHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        print request
        #user = User.objects.get(username=username)
        q = '+'+' +'.join(request.GET['q'].split(' '))
        exercises = Exercise.objects.filter(content__search=q)
        data = []
        for e in exercises[:100]:
            data.append({'sections':e.sections(),'path':e.path,'title':e.title,'description':e.description[:255],'id':e.id})
        return { 'query':q,'results': exercises.count(), 'exercises': data}