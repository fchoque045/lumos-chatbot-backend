from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.chat.models import Generico, Saludo, Despedida, Horario
from core.chat.serializers import *
import datetime
import re


class GenericoViewSet(viewsets.ModelViewSet):
    queryset = Generico.objects.all()
    serializer_class = GenericoSerializer

    def get_queryset(self, pk=None, **kwargs):
        '''
        Get generics by a given tipo or get all if it isn't specified.

        Returns a queryset
        '''
        queryset = super().get_queryset()
        query = self.kwargs
        try:
            queryset = queryset.filter(tipo=kwargs['tipo'])
        except KeyError as e:
            if query == {}:
                queryset = queryset.all()
            else:
                queryset = queryset.filter(id=int(query['pk']))
        return queryset

    def list(self, request):
        try:
            if request.GET['tipo']:
                tipo = request.GET.get('tipo')
                generico_serializer = self.get_serializer(
                    self.get_queryset(tipo=tipo), many=True)
        except:
            generico_serializer = self.get_serializer(
                self.get_queryset(), many=True)
        return Response(generico_serializer.data, status=status.HTTP_200_OK)


class BaseSaludoViewset(viewsets.ModelViewSet):

    def get_queryset(self, pk=None, **kwargs):
        '''
        Get saludos by a given horario or get all if it isn't specified.

        Returns a queryset
        '''
        queryset = super().get_queryset()
        query = self.kwargs
        try:
            queryset = queryset.filter(horario=self.get_horario())
        except KeyError as e:
            if query == {}:
                queryset = queryset.all()
            else:
                queryset = queryset.filter(id=int(query['pk']))
        return queryset

    def get_horario(self):
        '''        
        Return the id of the Horario.tipo (M,T,N) according to the time
        '''
        from datetime import datetime
        hora = datetime.now().time()
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
    list_bye = ['grcias', 'gracias', 'gracia' 'chau', 'ok']

    def is_bye(self, text):
        '''
        Args: text (str)

        Clean the text and Returns a boolean if text belongs to list of byes
        '''

        text = text.lower()  # lowercase, standardize
        list_text = text.split(' ')
        new_list = []
        p = re.compile(r'[a-z-áéíóúñ]+')  # search only words
        for word in list_text:
            # example  "mensaje...con" split = "mensaje con"
            word = ' '.join(p.findall(word))
            word = re.sub(r'([abdefghijkmopqsu-zÀ-ÿ])\1{1,}', r'\1', word)
            new_list.append(word)
        for word in new_list:
            if word in self.list_bye:
                return True
        return False

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        try:
            if request.GET['text']:
                text = request.GET.get('text')
                if self.is_bye(text):
                    print('es despedida')
                    serializer = self.get_serializer(
                        self.get_queryset(), many=True)
                    return Response(serializer.data)
                return Response({'message': f'el texto no indica una despedida'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(serializer.data)
