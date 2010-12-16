from django.conf.urls.defaults import *
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', 'documents.views.explore'),
    url(r'^documentos/$', 'documents.views.explore',name="documents-explore"),
    (r'^documento/', include('exercita.documents.urls')),
    #url(r'^documents/$', 'documents.views.explore',name="documents-explore"),
    url(r'^ejercicios/$', 'documents.views.explore',name="exercices-explore"),
    # (r'^exercita/', include('exercita.foo.urls')),s
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
