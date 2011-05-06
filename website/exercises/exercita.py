# coding: utf-8
from documents.models import Exercise
from settings import EXERCITA
import os
import re

def relative_path (path):
    if not(path.startswith(EXERCITA['PATH'])):
        return False
    return path[len(EXERCITA['PATH'])+1:-2].replace('/','.')
    
def real_path (path):
    return os.path.join(EXERCITA['PATH'], path.replace('.','/')+'.x')

latexAccents = [
  [ u"à", "\\`a" ], # Grave accent
  [ u"è", "\\`e" ],
  [ u"ì", "\\`\\i" ],
  [ u"ò", "\\`o" ],
  [ u"ù", "\\`u" ],
  [ u"ỳ", "\\`y" ],
  [ u"À", "\\`A" ],
  [ u"È", "\\`E" ],
  [ u"Ì", "\\`\\I" ],
  [ u"Ò", "\\`O" ],
  [ u"Ù", "\\`U" ],
  [ u"Ỳ", "\\`Y" ],
  [ u"á", "\\'a" ], # Acute accent
  [ u"é", "\\'e" ],
  [ u"í", "\\'\\i" ],
  [ u"ó", "\\'o" ],
  [ u"ú", "\\'u" ],
  [ u"ý", "\\'y" ],
  [ u"Á", "\\'A" ],
  [ u"É", "\\'E" ],
  [ u"Í", "\\'\\I" ],
  [ u"Ó", "\\'O" ],
  [ u"Ú", "\\'U" ],
  [ u"Ý", "\\'Y" ],
  [ u"â", "\\^a" ], # Circumflex
  [ u"ê", "\\^e" ],
  [ u"î", "\\^\\i" ],
  [ u"ô", "\\^o" ],
  [ u"û", "\\^u" ],
  [ u"ŷ", "\\^y" ],
  [ u"Â", "\\^A" ],
  [ u"Ê", "\\^E" ],
  [ u"Î", "\\^\\I" ],
  [ u"Ô", "\\^O" ],
  [ u"Û", "\\^U" ],
  [ u"Ŷ", "\\^Y" ],
  [ u"ä", "\\\"a" ],    # Umlaut or dieresis
  [ u"ë", "\\\"e" ],
  [ u"ï", "\\\"\\i" ],
  [ u"ö", "\\\"o" ],
  [ u"ü", "\\\"u" ],
  [ u"ÿ", "\\\"y" ],
  [ u"Ä", "\\\"A" ],
  [ u"Ë", "\\\"E" ],
  [ u"Ï", "\\\"\\I" ],
  [ u"Ö", "\\\"O" ],
  [ u"Ü", "\\\"U" ],
  [ u"Ÿ", "\\\"Y" ],
  [ u"ç", "\\c{c}" ],   # Cedilla
  [ u"Ç", "\\c{C}" ],
  [ u"œ", "{\\oe}" ],   # Ligatures
  [ u"Œ", "{\\OE}" ],
  [ u"æ", "{\\ae}" ],
  [ u"Æ", "{\\AE}" ],
  [ u"å", "{\\aa}" ],
  [ u"Å", "{\\AA}" ],
  [ u"–", "--" ],   # Dashes
  [ u"—", "---" ],
  [ u"ø", "{\\o}" ],    # Misc latin-1 letters
  [ u"Ø", "{\\O}" ],
  [ u"ß", "{\\ss}" ],
  [ u"¡", "{!`}" ],
  [ u"¿", "{?`}" ],
  [ u"\\", "\\\\" ],    # Characters that should be quoted
  [ u"~", "\\~" ],
  [ u"&", "\\&" ],
  [ u"$", "\\$" ],
  [ u"{", "\\{" ],
  [ u"}", "\\}" ],
  [ u"%", "\\%" ],
  [ u"#", "\\#" ],
  [ u"_", "\\_" ],
  [ u"≥", "$\\ge$" ],   # Math operators
  [ u"≤", "$\\le$" ],
  [ u"≠", "$\\neq$" ],
  [ u"©", "\copyright" ], # Misc
  [ u"ı", "{\\i}" ],
  [ u"µ", "$\\mu$" ],
  [ u"°", "$\\deg$" ],
  [ u"‘", "`" ],    #Quotes
#  [ u"’", "'" ],
  [ u"“", "``" ],
  [ u"”", "''" ],
  [ u"‚", "," ],
  [ u"„", ",," ],
  [ u"¿", "?`" ],
]

def string_replace(dict,text):
    keys = dict.keys()
    keys.sort()
    for n in keys:
        text = text.replace(n,dict[n])
    return text
  
def parse (content):
    translation_table = dict([(unicode(v),unicode(k)) for k, v in latexAccents])
    
    #print r.group(1).translate(translation_table)
    #print u"aá".translate(translation_table)
    #print content
    try:
        r = re.compile(r"\\exer{title}(?P<title>[^{]+)\\exer{/title}",re.DOTALL | re.MULTILINE)
        r = re.search(r,content)
        title = r.group('title').strip()
        try:
            title = string_replace(translation_table,title)
        except:
            pass
    except:
        title = ""
    
    try:
        r = re.compile(r"\\exer{statement}(?P<statement>.+)\\exer{/statement}",re.DOTALL | re.MULTILINE)
        r = re.search(r,content)
        #print string_replace(translation_table,r.group('statement'))
        statement = r.group('statement').strip()
        #print statement[:500]
        try:
            pattern = re.compile("\\\\exer{reference}{([^}]+)}", re.DOTALL | re.MULTILINE)
            statement = pattern.sub(lambda match:'['+match.group(1)+']',statement)
        except:
            pass
        try:
            pattern = re.compile("\\\\emph{([^}]+)}", re.DOTALL | re.MULTILINE)
            statement = pattern.sub(lambda match:match.group(1),statement)
        except:
            pass
        
        try:
            pattern = re.compile("\\\[a-z]+{/?([^}]+)}", re.DOTALL | re.MULTILINE)
            statement = pattern.sub("",statement)
        except:
            pass
        statement = statement.strip()
        #statement.replace('\\exer{reference}','')
        #statement.replace('\\exer{text}','')
        #statement = string_replace(translation_table,statement)
        try:
            statement = string_replace(translation_table,statement)
        except:
            pass
        try:
            pattern = re.compile("{(\w)}", re.DOTALL | re.MULTILINE)
            statement = pattern.sub(lambda match:match.group(1),statement)
        except:
            pass
    except:
        statement = ""

    return title, statement

from django.utils.encoding import smart_unicode
import codecs

def get_or_create(path,update=False):
    rel = relative_path(path)
    f = codecs.open(path, 'r' )
    content = f.read()
    #print content.decode('UTF-8') 
    import chardet
    det =  chardet.detect(content)
    #print det
    content = content.decode(det['encoding'])
    title, description = parse(content)
    
    #title = unicode(title,errors= 'ignore')
    #content = unicode(content,errors= 'ignore')
    #description = unicode(description,errors= 'ignore')
    #title = title.decode('utf-8','replace')
    #content = content.decode('utf-8','replace')
    
    #description = description.decode('utf-8')
    #print title
    #print description[:100]
    exercise, created = Exercise.objects.get_or_create(path=rel,defaults={"title":title,"content":content,"description":description})
    if not(created) and update:
        exercise.title = title
        exercise.content = content
        exercise.description = description
        exercise.save()
    
#r = real_path('talf.turing.quehace')
#r = real_path('programacion.codificacion.codigosLineales')
#r = '/Users/syrus/Proyectos/exercita/exercita-db/matematicas/discreta/combinatoria/cadenas/palindromos.x'
#r = real_path('matematicas.discreta.combinatoria.ferridiculo')
#get_or_create(r)