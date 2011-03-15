from django.conf.urls.defaults import *


urlpatterns = patterns('documents.views',
    #url(r'^$', 'explore',name="documents-explore"),
    url(r'^(?P<id>\d+)$', 'document',name="view-document"),
    url(r'^(?P<id>\d+)/editar$', 'edit',name="edit-document"),
    url(r'^(?P<id>\d+)/latex$', 'latex',name="view-document-latex"),
    url(r'^nuevo$', 'edit',{'id':1},name="new-document"),
    url(r'^(?P<id>\d+).pdf$', 'download',name="download-document"),
)
