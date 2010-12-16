from django import forms

TYPE_CHOICES = (
    ('exercices','Hoja de ejercicios'),
    ('practice','Practica'),
    ('exam','Examen'),
)

SYMETRY_CHOICES = (
    ('symmetric','Simetrica'),
    ('asymmetric','Asimetrica'),
)

NUMERATION_CHOICES = (
    ('numbers','Solo Numeros'),
    ('triangles','Numeros precedidos de triangulos'),
    ('roundboxes','Numeros en cajas redondeadas'),
)

DOC_PART_STYLE_CHOICES = (
    ('short','Corta'),
    ('itemize','Itemize'),
    ('enumerate','Numerados'),
    ('description','Con descripcion'),
    ('section','Section'),
    ('par','En un nuevo parrafo'),
    ('auto','Automatico'),
)

DOC_EXAMPLE_STYLE_CHOICES = (
    ('section','Section'),
    ('example','Precedidos de "Ejemplo"'),
    ('par','En un nuevo parrafo'),
    ('auto','Automatico'),
)

DOC_HINT_STYLE_CHOICES = (
    ('short','Corta'),
    ('par','En un nuevo parrafo'),
    ('hint','Precedido de "Pista"'),
    ('footnote','Nota a pie de pagina'),
    ('end','En "Pistas"'),
    ('auto','Automatico'),
)

DOC_BIBLIOGRAPHY_STYLE_CHOICES = (
    ('section','En la seccion "Notas Bibliograficas"'),
    ('bibliography','Precedido de "Notas Bibliograficas'),
    ('par','En un nuevo parrafo'),
    ('auto','Automatico'),
)

DOC_HISTORY_STYLE_CHOICES = (
    ('section','En la seccion "Notas historicas"'),
    ('history','Precedido de "Notas historicas"'),
    ('par','En un nuevo parrafo'),
    ('auto','Automatico'),
)

class DocumentForm(forms.Form):
    title = forms.CharField(max_length=50,label='Nombre')
    description = forms.CharField(widget=forms.Textarea,label='Descripcion')
    public = forms.BooleanField(required=False,label='Publico',help_text='Marca la casilla si quieres que este documento sea publico')
    
    #properties
    type = forms.CharField(widget=forms.RadioSelect(choices=TYPE_CHOICES),label='Tipo')
    heading = forms.BooleanField(required=False,label='Cabecera',help_text='Si esta marcado se anadira automaticamente una cabecera con todo el contenido relevante.')
    heading_symmetry = forms.CharField(widget=forms.RadioSelect(choices=SYMETRY_CHOICES),label='Simetria de la cabecera')
    numeration = forms.CharField(widget=forms.RadioSelect(choices=NUMERATION_CHOICES),label='Numeracion',help_text = 'Indica la forma de enumerar los ejericicios')
    
    #style
    doc_number = forms.CharField(label='Numero de Documento',help_text='La definicion general del documento, es el numero de hoja (1,2,etc.) o el cariz del examen (parcial de febrero)')
    doc_part_number = forms.CharField(label='Numero de Apartado')
    doc_title = forms.CharField(max_length=50,label='Titulo',help_text='Para indicar el titulo de la hoja. Por ejemplo, Condicionales, Memoria dinamica, Orden superior, etc.')
    doc_epilog = forms.CharField(widget=forms.Textarea,label='Epilogo')
    doc_part_style = forms.CharField(widget=forms.Select(choices=DOC_PART_STYLE_CHOICES),label='Apartados',help_text='Indica el formato en el que apareceran los apartados.')
    doc_example_style = forms.CharField(widget=forms.Select(choices=DOC_EXAMPLE_STYLE_CHOICES),label='Ejemplos',help_text='Indica el formato en el que apareceran los ejemplos.')
    doc_hint_style = forms.CharField(widget=forms.Select(choices=DOC_HINT_STYLE_CHOICES),label='Pistas',help_text='Indica el formato en el que apareceran las pistas.')
    doc_bibliography_style = forms.CharField(widget=forms.Select(choices=DOC_BIBLIOGRAPHY_STYLE_CHOICES),label='Biografia',help_text='Indica el formato en el que apareceran las notas bibliograficas.')
    doc_history_style = forms.CharField(widget=forms.Select(choices=DOC_HISTORY_STYLE_CHOICES),label='Historia',help_text='Indica el formato en el que apareceran las notas historicas.')
    
    #parameters
    date = forms.CharField(max_length=50,label='Fecha de Publicacion')
    academic_year = forms.CharField(label='Ano academico')
    subject = forms.CharField(label='Asignatura')
    semester = forms.CharField(label='Semestre')
    group = forms.CharField(label='Grupo')
    degree = forms.CharField(label='Titulacion')
    institution = forms.CharField(label='Institucion')