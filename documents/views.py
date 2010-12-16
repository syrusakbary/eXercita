# Create your views here.
from django.http import HttpResponse
#from django.shortcuts import render_to_response
from coffin.template import add_to_builtins
from documents.forms import DocumentForm

add_to_builtins('jinja2-mediasync.media')

from coffin.shortcuts import render_to_response
def explore(request):
    return render_to_response('documents/explore.html')
    
def document(request,id):
    return render_to_response('documents/document.html')

def edit(request,id):
    if request.method == 'POST': # If the form has been submitted...
        form = DocumentForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/guardado/') # Redirect after POST
    else:
        form = DocumentForm() # An unbound form

    return render_to_response('documents/edit.html', {
        'form': form,
    })

def download (request,id):
    return HttpResponse('Descarga del documento')
    
def find(request):
    '''
    [{title:'nombre',desc:'description',choices:[{name:'Ejemplo',abr:'solution'}]]
    
    '''
    pass