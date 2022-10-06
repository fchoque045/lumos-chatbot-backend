from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *

router = DefaultRouter()

router.register(r'saludo',SaludoViewSet,basename = 'saludos')
router.register(r'generico',GenericoViewSet,basename = 'genericos')
router.register(r'categoria',CategoriaViewSet,basename = 'categoras')
router.register(r'subcategoria',SubcategoriaViewSet,basename = 'subcategoras')
router.register(r'pregunta',PreguntaViewSet,basename = 'preguntas')
router.register(r'preguntasKeyword',PreguntaSimplifiedViewSet,basename = 'preguntas')

# Rutas anidadas
subcategoria_router = routers.NestedSimpleRouter(router, r'subcategoria', lookup='subcategoria')
subcategoria_router.register(r'pregunta', PreguntaSimplifiedViewSet, basename='pregunta')

subcategoria_anidada_router = routers.NestedSimpleRouter(router, r'subcategoria', lookup='subcategoria')
subcategoria_anidada_router.register(r'subcategoria', SubcategoriaViewSet, basename='subcategoria')

# urlpatterns = router.urls

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(subcategoria_router.urls)),
    path(r'', include(subcategoria_anidada_router.urls))
]