from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from exercises.handlers import ExercisesHandler
from documents.handlers import DocumentReadyHandler

from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#import nexus

#nexus.autodiscover()
#auth = HttpBasicAuthentication(realm="My Realm")
#ad = { 'authentication': auth }
exercises_resource = Resource(handler=ExercisesHandler)
documentready_resource = Resource(handler=DocumentReadyHandler)


from django.views.generic import TemplateView

    
urlpatterns = patterns('',
    # Example:
    url(r'^$',  TemplateView.as_view(template_name='main.haml'),name='main'),
    (r'^documentos/', include('documents.urls')),
    (r'^ejercicios/', include('exercises.urls')),
    #url(r'^documents/$', 'documents.views.explore',name="documents-explore"),
    #url(r'^ejercicios/$', 'documents.views.explore',name="exercices-explore"),
    url(r'^ejercicios.json$', exercises_resource,name='exercises_list_json'), 
    url(r'^documento_listo.json$', documentready_resource,name='document_ready'), 
    # (r'^exercita/', include('exercita.foo.urls')),s
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name':'registration/login.haml'}),
    url(r'^accounts/profile/$',  TemplateView.as_view(template_name='account.haml')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'template_name':'registration/logged_out.haml'}),

    # Uncomment the next line to enable the admin:
    url(r'', include('social_auth.urls')),
    (r'^admin/', include(admin.site.urls)),
    #('^nexus/', include(nexus.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/absolutepath'}),
    )