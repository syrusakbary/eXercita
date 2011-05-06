from django.conf.urls.defaults import *
from documents.views import DocumentDetailView
from django.views.generic import ListView
from models import Exercise
from views import *

urlpatterns = patterns('exercices.views',
    #url(r'^$', 'explore',name="documents-explore"),
    url(r'^$',ExerciseListView.as_view(), name="exercise_list"),
)
