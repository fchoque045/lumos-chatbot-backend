from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

# CATEGORY = [
#     ('DCAP', 'Docente que cursaron año pasado'),
#     ('IC',	'Incripcion al campus'),
#     ('IC',	'Inicio cursado'),
#     ('CD',	'Carga de datos'),
# ]

TYPE = [
    ('MBie', 'Mensaje Bienvenida'),
    ('MDesp', 'Mensaje Despedida'),
    ('MErr', 'Mensaje Error'),
    ('MDef', 'Mensaje Default'),
    ('MDesc', 'Mensaje Descripcion'),
]

class Generico(models.Model):
    """Model definition for Generico."""
    text = models.TextField(blank = False, null = True)
    type = models.CharField(max_length = 25, choices = TYPE)

    class Meta:
        """Meta definition for Generico."""
        verbose_name = 'generico'
        verbose_name_plural = 'genericos'

    def __str__(self):
        """Unicode representation of Generico."""
        return self.type


class Categoria(models.Model):
    """Model definition for Categoria."""
    descripcion = models.CharField(max_length = 255, blank = False, null = False)
    nombre_corto = models.CharField(max_length = 10, blank = False, null = False)

    class Meta:
        """Meta definition for Categoria."""
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        """Unicode representation of Categoria."""
        return self.nombre_corto

class SubCategoria(models.Model):
    """Model definition for Categoria."""
    descripcion = models.CharField(max_length = 255, blank = False, null = False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null = True)
    subcategoria = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name = '+')

    class Meta:
        """Meta definition for Subategoria."""
        verbose_name = 'subcategoria'
        verbose_name_plural = 'subcategorias'

    def __str__(self):
        """Unicode representation of Subategoria."""
        return self.descripcion

class Keyword(models.Model):
    """Model definition for Keyword."""
    text = models.CharField(max_length = 255, blank = False, null = False)    

    class Meta:
        """Meta definition for Keyword."""
        verbose_name = 'keyword'
        verbose_name_plural = 'keywords'

    def __str__(self):
        """Unicode representation of Keyword."""
        return self.text

class Pregunta(models.Model):
    """Model definition for Pregunta."""
    pregunta = models.TextField()
    respuesta = RichTextField()
    keyword = models.ManyToManyField(Keyword, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank=True, null=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        """Meta definition for Pregunta."""
        verbose_name = 'pregunta'
        verbose_name_plural = 'preguntas'

    def __str__(self):
        """Unicode representation of Pregunta."""
        return self.pregunta

    def get_keywords(self):
        return "\n".join([k.pregunta + ',' for k in self.keyword.all()])