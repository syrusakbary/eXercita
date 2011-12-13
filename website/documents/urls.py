from django.conf.urls.defaults import *
from documents.views import DocumentDetailView
from django.views.generic import ListView
from documents.models import Document


urlpatterns = patterns('documents.views',
    #url(r'^$', 'explore',name="documents-explore"),
    url(r'^$',ListView.as_view(model=Document,template_name="documents/document_list.jade"), name="document_list"),
    url(r'^(?P<pk>\d+)$',DocumentDetailView.as_view(),name="document_detail"),
    url(r'^(?P<pk>\d+)/editar$', 'edit',name="document_edit"),
    url(r'^(?P<pk>\d+)/descargar/(?P<format>pdf|latex)', 'download',name="document_download"),
    url(r'^(?P<pk>\d+)/thumb/(?P<size>\w+)/(?P<i>\d+)$', 'thumb',name="document_thumb"),
    url(r'^nuevo$', 'edit',name="document_create"),
    #url(r'^(?P<pk>\d+)/descarga$', 'download',name="document_download"),
)
