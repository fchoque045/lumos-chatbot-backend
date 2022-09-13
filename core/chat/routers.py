from rest_framework.routers import DefaultRouter
from .views import GenericoViewSet, CategoriaViewSet, SubcategoriaViewSet, PreguntaViewSet

router = DefaultRouter()

router.register(r'generico',GenericoViewSet,basename = 'genericos')
router.register(r'categoria',CategoriaViewSet,basename = 'categoras')
router.register(r'subcategoria',SubcategoriaViewSet,basename = 'subcategoras')
router.register(r'pregunta',PreguntaViewSet,basename = 'preguntas')

urlpatterns = router.urls