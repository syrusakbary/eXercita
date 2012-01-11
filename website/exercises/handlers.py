from piston.handler import BaseHandler
from piston.utils import rc, throttle
from models import Exercise
from haystack.query import SearchQuerySet
from django.core.urlresolvers import reverse

class ExercisesHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        #print request
        #user = User.objects.get(username=username)
        baseq = q = request.GET['q']
        if q == '': return {}
        q += '*'
        p = int(request.GET.get('p',1))
        show = 10
        init = (p-1)*show
        end = init+show
        #raise Exception (q)
        if False:
            q = ' '.join(['+'+i+'*' for i in request.GET['q'].split(' ')])
            exercises = Exercise.objects.filter(content__search=q)
            data = []
            for e in exercises[p*show:(p+1)*show]:
                data.append({'sections':e.sections(),'path':e.path,'title':e.title,'description':e.description[:255],'id':e.id})
            count = exercises.count()
        else:
            s = SearchQuerySet().raw_search(q).highlight()
            count = s.count()
            data = []
            for e in s[init:end]:
                data.append({'sections':e.object.sections(),'path':e.object.path,'title':e.title,'description':e.highlighted[0],'id':e.object.id})
        return { 'query':q,'page':p+1,'results': count, 'exercises': data,'more':'%s?q=%s&p=%d'%(reverse('exercises_list_json'),baseq,p+1) if end<count else False}