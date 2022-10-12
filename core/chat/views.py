from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.chat.models import Generico, Categoria, Saludo, Despedida, SubCategoria, Pregunta, Keyword
from core.chat.serializers import *

import re

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

class SaludoViewSet(viewsets.ModelViewSet):
    queryset = Saludo.objects.all()
    serializer_class = SaludoSerializer

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

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CaterogiaSerializer

class SubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = SubCategoria.objects.all()
    serializer_class = SubcaterogiaSerializer

    def get_queryset(self,pk=None):
        queryset = super().get_queryset()
        query = self.kwargs
        print(query)
        if query == {}:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(subcategoria = int(query['subcategoria_pk']))
        return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     query = self.kwargs
    #     if query == {}:
    #         queryset = queryset.all()

    #     print(query)
    #     # {'group_pk': '1'}
    #     # {'pk': '1'}
    #     if len(query) == 1:
    #         try:
    #             queryset = queryset.filter(group = self.kwargs['group_pk'])
    #         except KeyError:
    #             queryset = queryset.filter(id = self.kwargs['pk'])
        
    #     # {'group_pk': '1', 'pk': '3'}
    #     if len(query) == 2:
    #         queryset = queryset.filter(group = int(query['group_pk']))
    #         queryset = queryset.filter(id = self.kwargs['pk'])

    #     return queryset

class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

class PreguntaSubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSimplifiedSerializer

    def get_queryset(self,pk=None):
        queryset = super().get_queryset()
        query = self.kwargs
        print(query)
        if query == {}:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(subcategoria = int(query['subcategoria_pk']))
        return queryset

class PreguntaKeywordViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSimplifiedSerializer

    def get_queryset(self, pk=None, **kwargs):
        queryset = super().get_queryset()
        try:
            keyword = Keyword.objects.get(text=kwargs['keyword'])
            return Pregunta.objects.filter(keyword = keyword.id)
        except KeyError as e:
            queryset = queryset.all()
        return queryset

    def list(self,request):
        print('lista de preguntas')
        try:            
            text_clean = self.get_cleantext(request.GET.get('keyword'))
            keyword = self.get_key(text_clean)
            if keyword is None:
                return Response({'message':f'No se encuentra preguntas referidas a la keyword'}, status=status.HTTP_404_NOT_FOUND)
            pregunta_serializer = self.get_serializer(self.get_queryset(keyword=keyword),many = True)
            return Response(pregunta_serializer.data, status = status.HTTP_200_OK)
        except:
            return Response({'message': f'debe ingresar una keyword como parametro'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_key(self, list_text):
        queryset_keywords = list(Keyword.objects.all())
        keywords = [k.text for k in queryset_keywords]
        for word in list_text:
            if word in keywords:
                return word
        return None

    def get_cleantext(self,text):
        '''Get text(comment). Returns the clean text'''
        text = text.lower() #lowercase, standardize
        list_text = text.split(' ')
        new_list = []
        p = re.compile(r'[a-z-áéíóúñ]+')#search only words
        for word in list_text:
            word = ' '.join(p.findall(word)) #example  "mensaje...con" split = "mensaje con"
            word = re.sub(r'([abdefghijkmopqsu-zÀ-ÿ])\1{1,}', r'\1', word)      
            new_list.append(word)
        return new_list