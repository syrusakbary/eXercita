"""
See http://docs.djangoproject.com/en/dev/ref/templates/api/#using-an-alternative-template-language

Use:
 * {{ url_for('view_name') }} instead of {% url view_name %},
 * <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
   instead of {% csrf_token %}.

"""

from django.template.loader import BaseLoader
from django.template.loaders.app_directories import app_template_dirs
from django.template import TemplateDoesNotExist
from django.core import urlresolvers
from django.conf import settings
import jinja2

class Template(jinja2.Template):
    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        return super(Template, self).render(context_dict)

class Loader(BaseLoader):
    is_usable = True
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(app_template_dirs))
    env.template_class = Template

    # These are available to all templates.
    #env.globals['url'] = rev
    env.globals['MEDIA_URL'] = settings.MEDIA_URL
    #env.globals['STATIC_URL'] = settings.STATIC_URL
    

    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.env.get_template(template_name)
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)
        return template, template.filename

def rev(viewname,*args,**kwargs):
    return urlresolvers.reverse(viewname,args=args,kwargs=kwargs)

from mediasync.templatetags.media import *



Loader.env.globals['url'] = rev

def make_jinja2_tag(node,*args,**kwargs):
    def f(*args,**kwargs):
        return node(*args,**kwargs).render({})
    return f
from django.template.defaulttags import CsrfTokenNode
from jinja2 import Markup

def csrf_token(csrf_token=""):
    from django.template.defaulttags import CsrfTokenNode
    return Markup(CsrfTokenNode().render({'csrf_token': csrf_token}))

Loader.env.globals['media_url'] = make_jinja2_tag(MediaUrlTagNode)
Loader.env.globals['css'] = make_jinja2_tag(CssTagNode)
Loader.env.globals['js'] = make_jinja2_tag(JsTagNode)
Loader.env.globals['csrf_token'] = csrf_token