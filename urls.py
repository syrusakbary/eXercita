from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from documents.handlers import ExercisesHandler

import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#import nexus

#nexus.autodiscover()
#auth = HttpBasicAuthentication(realm="My Realm")
#ad = { 'authentication': auth }
ad = {}
exercises_resource = Resource(handler=ExercisesHandler, **ad)

urlpatterns = patterns('',
    # Example:
    url(r'^$', 'documents.views.explore'),
    url(r'^documentos/$', 'documents.views.explore',name="documents-explore"),
    (r'^documento/', include('exercita.documents.urls')),
    #url(r'^documents/$', 'documents.views.explore',name="documents-explore"),
    url(r'^ejercicios/$', 'documents.views.explore',name="exercices-explore"),
    url(r'^ejercicios.json$', exercises_resource), 
    # (r'^exercita/', include('exercita.foo.urls')),s
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #('^nexus/', include(nexus.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/absolutepath'}),
    )