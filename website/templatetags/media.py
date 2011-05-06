from djinja import template
from mediasync.templatetags.media import MediaUrlTagNode,CssTagNode,JsTagNode
from djinja.template.loaders import make_jinja2_tag

register = template.Library()

register.tag(make_jinja2_tag(MediaUrlTagNode),name='media_url')
register.tag(make_jinja2_tag(CssTagNode),name='css')
register.tag(make_jinja2_tag(JsTagNode),name='js')
