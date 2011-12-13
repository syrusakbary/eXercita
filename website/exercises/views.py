from django.views.generic import ListView, DetailView
from models import *

# Create your views here.
class ExerciseListView(ListView):
    template_name='exercises/exercise_list.jade'
    queryset = Exercise.objects.all()[:30]
