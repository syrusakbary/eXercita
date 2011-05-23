from django.core.management.base import BaseCommand, CommandError
from optparse import OptionParser, make_option
from exercises.models import Exercise
from exercises.exercita import *
import os

class Command(BaseCommand):
    args = 'name'
    help = 'Crea (o actualiza) los datos de cada ejercicio de eXercita'
    option_list = BaseCommand.option_list + (
        make_option('-n','--new',
            dest='static',
            default=False,
            help='Crear una nueva tabla de ejercicios'),
        make_option('-U','--update',
            dest='update',
            default=True,
            help='Actualizar la tabla de ejercicios'),
    )
    def walk_dir(self,path):
        F = []
        for top, dirs, files in os.walk(path):
            for f in files:      
                if f.endswith('.x'):
                    F.append(os.path.join(top, f))
            for d in dirs:
                F += self.walk_dir(os.path.join(top, d))
        return F
    def handle(self, *args, **options):
        from django.template import Context, Template
        from settings import EXERCITA
        files = self.walk_dir(EXERCITA['DATABASE'])
        print files
        for f in files:
            get_or_create(f,update=options['update'])
            
        # import os
#         
#         name = args[0]
#         wsgi = os.path.join(ROOT_PATH,name+'.wsgi')
#         conf = os.path.join(ROOT_PATH,name+'.conf')
#         
#         f_wsgi = open(wsgi, 'w')
#         c_wsgi = Template(WSGI_CONFIG).render(Context({
#             'sitedir':      ROOT_PATH
#         }))
#         f_wsgi.write(c_wsgi)
#         f_wsgi.close()
# 
#         f_conf = open(conf, 'w')
#         from distutils.sysconfig import get_python_lib
#         c_conf = Template(TEMPLATE_CONFIG).render(Context({
#             'host':         options['host'],
#             'pythonpath':   get_python_lib(),
#             'wsgi':         wsgi,
#             'process':      name
#         }))
#         f_conf.write(c_conf)
#         f_conf.close()