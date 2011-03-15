# Create your views here.
from django.http import HttpResponse
#from django.shortcuts import render_to_response
#from coffin.template import add_to_builtins
from django.shortcuts import render_to_response
from django.template import add_to_builtins
from documents.models import *
add_to_builtins('mediasync.templatetags.media')
#add_to_builtins('exercita.documents.templatetags.documents_tags')

from documents.forms import DocumentForm

#add_to_builtins('jinja2-mediasync.media')

#from coffin.shortcuts import render_to_response
def explore(request):
    return render_to_response('documents/explore.html')
    
def document(request,id):
    return render_to_response('documents/document.html')

def get_exercises (e):
    e = e.split(';')
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

def latex (request,id):
    d= Document.objects.get(id=id)
    return render_to_response('documents/exercita.html', {'data':d.data,'exercises':get_exercises(d.data['exercises'])})
     
def edit(request,id):
    from django.utils import simplejson
    if request.method == 'POST': # If the form has been submitted...
        data = request.POST
        form = DocumentForm(data) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            try:
                d= Document.objects.get(id=1)
            except:
                d = Document()
            d.data = form.cleaned_data
            d.title = form.cleaned_data['title']
            d.description = form.cleaned_data['description']
            d.public = form.cleaned_data['public']
            #d.author = request.user
            d.save()
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponse(sections)
            #return HttpResponse(simplejson.dumps(form.cleaned_data))
            
        return render_to_response('documents/edit.html', {
            'form': form,
            'exercises':simplejson.dumps(get_exercises(data['exercises'])),
        })
    else:
        try:
            d= Document.objects.get(id=1)
            d = d.data
            exercises = simplejson.dumps(get_exercises(d['exercises']))
        except:
            d = {}
            exercises = False
        form = DocumentForm(d) # An unbound form
    #return HttpResponse(simplejson.dumps(get_exercises(d['exercises'])))
    return render_to_response('documents/edit.html', {
        'form': form,
        'exercises':exercises,
    })

def download (request,id):
    return HttpResponse('Descarga del documento')
    
def find(request):
    '''
    [{title:'nombre',desc:'description',choices:[{name:'Ejemplo',abr:'solution'}]]
    
    '''
    pass