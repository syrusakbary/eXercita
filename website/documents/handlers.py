from piston.handler import BaseHandler
from piston.utils import rc, throttle
from models import Document

class DocumentReadyHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        final = Document.objects.filter(pk=request.GET['id']).exclude(state='PR').exists()
        return { 'ready':final}