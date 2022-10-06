from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'saludo',SaludoViewSet,basename = 'saludos')
router.register(r'generico',GenericoViewSet,basename = 'genericos')
router.register(r'categoria',CategoriaViewSet,basename = 'categoras')
router.register(r'subcategoria',SubcategoriaViewSet,basename = 'subcategoras')
router.register(r'pregunta',PreguntaViewSet,basename = 'preguntas')

urlpatterns = router.urls