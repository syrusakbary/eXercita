import threading
import os
import re
from subprocess import call, PIPE, Popen

class CreateRelated(threading.Thread):
    def __init__(self, instance):
        self.instance = instance
        threading.Thread.__init__(self)

    def run (self):
        base = self.instance.base()
        try:
            os.makedirs(base)
        except OSError:
            pass
        #self.instance.pk,
        self.make_latex()
        self.make_dvi()
        self.make_images()
        self.instance.save(create_related=False)

    def make_latex(self):
        latex = open ( self.instance.file('document.x'), 'w' )
        latex.write (self.instance.latex() )
        latex.close() 


    def make_dvi(self):
        pass
        #s = Popen(['latex', 'document.x'],cwd=self.instance.base(), stdout=PIPE, stderr=PIPE).communicate()[0]
    def make_pdf(self):
        pass
        #s = Popen(['dvipdfm', 'document.dvi','-o','document.pdf'],cwd=self.instance.base(), stdout=PIPE, stderr=PIPE).communicate()[0]

    def make_images(self):
        s = Popen(['dvipng', 'document.dvi','-o','preview_%d.png'],cwd=self.instance.base(), stdout=PIPE, stderr=PIPE).communicate()[0]
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
                im.thumbnail(size, Image.ANTIALIAS)
                background = Image.new('RGBA', size, (255, 255, 255, 0))
                background.paste(im, ((size[0] - im.size[0]) / 2, (size[1] - im.size[1]) / 2))
                background.save(self.instance.image(p+1,size), 'PNG')
        