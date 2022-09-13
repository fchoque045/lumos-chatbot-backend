from django.contrib import admin
from .models import Generico, Categoria, SubCategoria, Pregunta, Keyword

# Register your models here.
class GenericoAdminConfig(admin.ModelAdmin):
    model = Generico
    search_fields = ('text', 'type')
    ordering = ('id',)
    list_display = ('id', 'text', 'type' )

class CategoriaAdminConfig(admin.ModelAdmin):
    model = Categoria
    search_fields = ('descripcion','nombre_corto')
    ordering = ('id',)
    list_display = ('id', 'descripcion', 'nombre_corto' )

class SubcategoriaAdminConfig(admin.ModelAdmin):
    model = SubCategoria
    search_fields = ('descripcion', 'categoria')
    ordering = ('id',)
    list_display = ('id', 'descripcion', 'categoria', 'subcategoria')

class PreguntaAdminConfig(admin.ModelAdmin):
    model = Pregunta
    search_fields = ('pregunta', 'respuesta', 'categoria')
    list_display = ('id', 'pregunta', 'respuesta', 'categoria','subcategoria', 'get_keywords',)
    ordering = ('id',)

class KeywordAdminConfig(admin.ModelAdmin):
    model = Keyword
    search_fields = ('text',)
    list_display = ('id', 'text',)
    ordering = ('id',)

admin.site.register(Generico, GenericoAdminConfig)
admin.site.register(Categoria, CategoriaAdminConfig)
admin.site.register(SubCategoria, SubcategoriaAdminConfig)
admin.site.register(Pregunta, PreguntaAdminConfig)
admin.site.register(Keyword, KeywordAdminConfig)
