from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from core.chat.views.generico.views import *
from core.chat.views.pregunta.views import *

router = DefaultRouter()

router.register(r'saludo',SaludoViewSet,basename = 'saludos')
router.register(r'despedida',DespedidaViewSet,basename = 'despedidas')
router.register(r'generico',GenericoViewSet,basename = 'genericos')
router.register(r'categoria',CategoriaViewSet,basename = 'categoras')
router.register(r'subcategoria',SubcategoriaViewSet,basename = 'subcategorias')
router.register(r'pregunta',PreguntaViewSet,basename = 'preguntas')
router.register(r'preguntaKeyword',PreguntaKeywordViewSet,basename = 'preguntasKeywords')

# Rutas anidadas
subcategoria_router = routers.NestedSimpleRouter(router, r'subcategoria', lookup='subcategoria')
subcategoria_router.register(r'pregunta', PreguntaSubcategoriaViewSet, basename='pregunta')

subcategoria_anidada_router = routers.NestedSimpleRouter(router, r'subcategoria', lookup='subcategoria')
subcategoria_anidada_router.register(r'subcategoria', SubcategoriaViewSet, basename='subcategoria')

# urlpatterns = router.urls

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(subcategoria_router.urls)),
    path(r'', include(subcategoria_anidada_router.urls))
]