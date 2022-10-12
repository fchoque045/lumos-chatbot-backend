from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.chat.models import Generico, Saludo, Despedida, Horario
from core.chat.serializers import *


class GenericoViewSet(viewsets.ModelViewSet):
    queryset = Generico.objects.all()
    serializer_class = GenericoSerializer

    def get_queryset(self,pk=None, **kwargs):
        queryset = super().get_queryset()
        query = self.kwargs
        try:
            queryset = queryset.filter(tipo = kwargs['tipo'])
        except KeyError as e:
            if query == {}:
                queryset = queryset.all()
            else:
                queryset = queryset.filter(id = int(query['pk']))
        return queryset
    
    def list(self,request):
        try: 
            if request.GET['tipo']:
                tipo = request.GET.get('tipo')
                generico_serializer = self.get_serializer(self.get_queryset(tipo=tipo),many = True)
        except:
            generico_serializer = self.get_serializer(self.get_queryset(),many = True)
        return Response(generico_serializer.data, status = status.HTTP_200_OK)


class BaseSaludoViewset(viewsets.ModelViewSet):

    def get_queryset(self,pk=None, **kwargs):
        queryset = super().get_queryset()
        query = self.kwargs
        try:
            queryset = queryset.filter(horario = self.get_horario(kwargs['hora']))
        except KeyError as e:
            if query == {}:
                queryset = queryset.all()
            else:
                queryset = queryset.filter(id = int(query['pk']))
        return queryset

    def list(self,request):
        try:
            hora = request.GET.get('hora')
            saludo_serializer = self.get_serializer(self.get_queryset(hora=hora),many = True)
        except:
            saludo_serializer = self.get_serializer(self.get_queryset(),many = True)
            
        return Response(saludo_serializer.data, status = status.HTTP_200_OK)

    def get_horario(self, hora_string):
        import datetime
        hours, minutes = tuple(hora_string.split(":"))
        hora = datetime.time(int(hours), int(minutes), 0)
        horarios = Horario.objects.order_by('hora')
        if hora >= horarios[0].hora and hora <= horarios[1].hora:
            tipo = horarios[0]
        elif hora >= horarios[1].hora and hora <= horarios[2].hora:
            tipo = horarios[1]
        else:
            tipo = horarios[2]
        return tipo.id

class SaludoViewSet(BaseSaludoViewset):
    queryset = Saludo.objects.all()
    serializer_class = SaludoSerializer

class DespedidaViewSet(BaseSaludoViewset):
    queryset = Despedida.objects.all()
    serializer_class = DespedidaSerializer

    