# coding: utf-8
from django import forms

TYPE_CHOICES = (
    ('exercices','Hoja de ejercicios'),
    ('practice','Práctica'),
    ('exam','Examen'),
)

SYMETRY_CHOICES = (
    ('symmetric','Simétrica'),
    ('asymmetric','Asimétrica'),
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
    ('par','En un nuevo párrafo'),
    ('auto','Automático'),
)

DOC_EXAMPLE_STYLE_CHOICES = (
    ('section','Section'),
    ('example','Precedidos de "Ejemplo"'),
    ('par','En un nuevo parrafo'),
    ('auto','Automatico'),
)

DOC_HINT_STYLE_CHOICES = (
    ('short','Corta'),
    ('par','En un nuevo párrafo'),
    ('hint','Precedido de "Pista"'),
    ('footnote','Nota a pie de pagina'),
    ('end','En "Pistas"'),
    ('auto','Automático'),
)

DOC_BIBLIOGRAPHY_STYLE_CHOICES = (
    ('section','En la seccion "Notas Bibliográficas"'),
    ('bibliography','Precedido de "Notas Bibliográficas'),
    ('par','En un nuevo párrafo'),
    ('auto','Automático'),
)

DOC_HISTORY_STYLE_CHOICES = (
    ('section','En la seccion "Notas históricas"'),
    ('history','Precedido de "Notas históricas"'),
    ('par','En un nuevo párrafo'),
    ('auto','Automático'),
)

class DocumentForm(forms.Form):

    title = forms.CharField(max_length=50,label='Nombre')
    description = forms.CharField(widget=forms.Textarea,label='Descripción')
    public = forms.BooleanField(required=False,label='Público',help_text='Marca la casilla si quieres que este documento sea público')
    
    #properties
    type = forms.CharField(widget=forms.RadioSelect(choices=TYPE_CHOICES),label='Tipo')
    heading = forms.BooleanField(required=False,label='Cabecera',help_text='Si esta marcado se añadira automáticamente una cabecera con todo el contenido relevante.')
    heading_symmetry = forms.CharField(widget=forms.RadioSelect(choices=SYMETRY_CHOICES),label='Simetría de la cabecera',required=False )
    numeration = forms.CharField(widget=forms.RadioSelect(choices=NUMERATION_CHOICES),label='Numeración',help_text = 'Indica la forma de enumerar los ejericicios',required=False)
    
    #style
    doc_number = forms.CharField(label='Número de Documento',help_text='La definición general del documento, es el numero de hoja (1,2,etc.) o el cariz del examen (parcial de febrero)',required=False)
    doc_part_number = forms.CharField(label='Número de Apartado',required=False)
    doc_title = forms.CharField(max_length=50,label='Título',help_text='Para indicar el título de la hoja. Por ejemplo, Condicionales, Memoria dinámica, Orden superior, etc.')
    doc_epilog = forms.CharField(widget=forms.Textarea,label='Epilogo',required=False)
    doc_part_style = forms.CharField(widget=forms.Select(choices=DOC_PART_STYLE_CHOICES),label='Apartados',help_text='Indica el formato en el que apareceran los apartados.',required=False)
    doc_example_style = forms.CharField(widget=forms.Select(choices=DOC_EXAMPLE_STYLE_CHOICES),label='Ejemplos',help_text='Indica el formato en el que apareceran los ejemplos.',required=False)
    doc_hint_style = forms.CharField(widget=forms.Select(choices=DOC_HINT_STYLE_CHOICES),label='Pistas',help_text='Indica el formato en el que apareceran las pistas.',required=False)
    doc_bibliography_style = forms.CharField(widget=forms.Select(choices=DOC_BIBLIOGRAPHY_STYLE_CHOICES),label='Biografia',help_text='Indica el formato en el que apareceran las notas bibliograficas.',required=False)
    doc_history_style = forms.CharField(widget=forms.Select(choices=DOC_HISTORY_STYLE_CHOICES),label='Historia',help_text='Indica el formato en el que apareceran las notas historicas.',required=False)
    
    #parameters
    date = forms.CharField(max_length=50,label='Fecha de Publicación',required=False)
    academic_year = forms.CharField(label='Año academico',required=False)
    subject = forms.CharField(label='Asignatura',required=False)
    semester = forms.CharField(label='Semestre',required=False)
    group = forms.CharField(label='Grupo',required=False)
    degree = forms.CharField(label='Titulación',required=False)
    institution = forms.CharField(label='Institución',required=False)
    
    exercises = forms.CharField(widget=forms.HiddenInput(),required=True,error_messages={'required': u'No ha seleccionado ningún ejericicio'})
