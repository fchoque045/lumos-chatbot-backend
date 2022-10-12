from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from core.chat.models import Categoria, SubCategoria, Pregunta, Keyword
from core.chat.serializers import *

import re
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