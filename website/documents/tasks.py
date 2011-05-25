import threading
import os
import re
from subprocess import call, PIPE, Popen

class CreateRelated(threading.Thread):
    def __init__(self, instance):
        self.instance = instance
        threading.Thread.__init__(self)

    def run (self):
        self.base = self.instance.base()
        try:
            os.makedirs(self.base)
            os.chmod(self.base,0o777)
        except OSError:
            pass
        #self.instance.pk,
        import traceback
        import StringIO
        try:
            self.instance.data['traceback'] = ''
            self.make_latex()
            self.make_dvi()
            self.make_pdf()
            self.make_images()
            self.instance.state = 'OK'
        except Exception as e:
            self.instance.state = 'ER'
            self.instance.data['error'] = e
            s=StringIO.StringIO()
            traceback.print_exc(file=s)
            s.seek(0)
            self.instance.data['traceback'] = s.read()
        finally:
            self.instance.save(create_related=False)

    def make_latex(self):
        import codecs
        latex = codecs.open ( self.instance.file('document.tex'), encoding='utf-8', mode='w+' )
        latex.write (unicode(self.instance.latex()) )
        latex.close() 


    def make_dvi(self):
        s = Popen(['latex', 'document.tex'],cwd=self.base, stdout=PIPE, stderr=PIPE,env={"TEXINPUTS": ":/usr/share/exercita//:/usr/share/exercita-db/"}).communicate()[0]
    def make_pdf(self):
        #pass
        #,'-o','document.pdf'
        s = Popen(['dvipdfm', 'document.dvi'],cwd=self.instance.base(), stdout=PIPE, stderr=PIPE).communicate()[0]

    def make_images(self):
        #/opt/local/bin/dvipng
        s = Popen(['dvipng', 'document.dvi','-o','preview_%d.png'],cwd=self.base, stdout=PIPE, stderr=PIPE).communicate()[0]
        pattern = re.compile("\[(\d+)\]")
        images = pattern.findall(s)
        pages = len(images)
        self.instance.pages = pages
        
        try:
            from PIL import Image, ImageOps
        except ImportError:
            import Image
            import ImageOps
            
        from documents.models import IMAGE_SIZE
        sizes = IMAGE_SIZE.values()
        for p in range(pages):
            image = Image.open(self.instance.file('preview_%s.png'%images[p]))
            for size in sizes:
                im = image.copy()
                im = im.convert("RGB")
                
                basewidth = size[1]
                wpercent = (basewidth/float(im.size[1]))
                hsize = int((float(im.size[0])*float(wpercent)))
                im = im.resize((hsize,basewidth),Image.ANTIALIAS)
                
                background = Image.new('RGB', size, (255, 255, 255))
                background.paste(im, ((size[0] - im.size[0]) / 2, (size[1] - im.size[1]) / 2))
                background.save(self.instance.image(p+1,size), 'PNG')
        