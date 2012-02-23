# Create your views here.
from django.http import HttpResponse
#from django.shortcuts import render_to_response
#from coffin.template import add_to_builtins
from django.shortcuts import render_to_response
from django.template import add_to_builtins
from exercises.models import *
from documents.models import *

#add_to_builtins('mediasync.templatetags.media')
#add_to_builtins('exercita.documents.templatetags.documents_tags')

from documents.forms import DocumentForm
from django.contrib.auth.decorators import permission_required

#add_to_builtins('jinja2-mediasync.media')
from django.views.generic import DetailView
from django.template import RequestContext

from django.shortcuts import redirect

class DocumentDetailView(DetailView):
    queryset = Document.objects.all()
    template_name = template_name="documents/document_detail.jade"
#      def get_object(self):
#         # Call the superclass
#         object = super(AuthorDetailView, self).get_object()
#         # Record the last accessed date
#         object.last_accessed = datetime.datetime.now()
#         object.save()
#         # Return the object
#         return object
        
#from coffin.shortcuts import render_to_response
def explore(request):
    return render_to_response('documents/explore.jade')
    
def document(request,pk):
    return render_to_response('documents/document.jade')

def get_exercises (e):
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

def prueba (request,pk):
    d= Document.objects.get(id=pk)
    return HttpResponse(d.latex())

def thumb(request,pk,size,i):
    from settings import EXERCITA
    import os
    response = HttpResponse(mimetype="image/png")
    try:
        from PIL import Image, ImageOps
    except ImportError:
        import Image
#        import ImageOps
    from documents.models import IMAGE_SIZE
    size = IMAGE_SIZE[size]
    image =  os.path.join(EXERCITA['DOCUMENTS'],str(pk),'thumbnail_%s_%d_%d.png'%(i-1,size[0],size[1]))
    img = Image.open(image)
    img.save(response, "PNG")
    return response

from django.contrib.auth.decorators import login_required
    
@login_required
def edit(request,pk=False):
    from django.utils import simplejson
    if not(pk):
        doc = Document()
    else:
        doc = Document.objects.get(id=pk)
    if request.method == 'POST': # If the form has been submitted...
        data = request.POST
        form = DocumentForm(data) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            doc.data = form.cleaned_data
            doc.title = form.cleaned_data['title']
            doc.description = form.cleaned_data['description']
            #doc.public = form.cleaned_data['public']
            doc.author = request.user
            doc.save()
            
            return redirect('document_detail', pk=doc.pk)
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponse(sections)
            #return HttpResponse(simplejson.dumps(form.cleaned_data))
        #doc.data = form.cleaned_data
        exercises = simplejson.dumps(doc.exercises())
    elif not(pk):
        exercises = False
        form = DocumentForm()
    else:
        d = doc.data
        if type(d) != dict: d = {}
        exercises = simplejson.dumps(doc.exercises())
        form = DocumentForm(d) # An unbound form
    #return HttpResponse(simplejson.dumps(get_exercises(d['exercises'])))
    return render_to_response('documents/document_edit.jade', {
        'form': form,
        'exercises':exercises,
    },RequestContext(request))


def create(request):
    from django.utils import simplejson
    if request.method == 'POST': # If the form has been submitted...
        data = request.POST
        form = DocumentForm(data) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
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
        exercises = simplejson.dumps(get_exercises(data['exercises']))
        
    else:
        d = {}
        exercises = False
        form = DocumentForm()
    return render_to_response('documents/document_edit.jade', {
        'form': form,
        'exercises':exercises,
    },RequestContext(request))
# An unbound form
#    return HttpResponse(simplejson.dumps(get_exercises(d['exercises'])))
    

def download (request,pk,format):
    from sendfile import sendfile
    document = Document.objects.get(id=pk)
    file = document.path(format)
    return sendfile(request, file, attachment=True)
    #return HttpResponse('Descarga del documento')
    
def find(request):
    '''
    [{title:'nombre',desc:'description',choices:[{name:'Ejemplo',abr:'solution'}]]
    
    '''
    pass