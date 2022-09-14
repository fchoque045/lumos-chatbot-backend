from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from core.chat.models import Generico, Categoria, SubCategoria, Pregunta, Keyword
from core.chat.serializers import GenericoSerializer, CaterogiaSerializer, SubcaterogiaSerializer, PreguntaSerializer

import re

class GenericoListAPIView(ListAPIView):
    queryset = Generico.objects.all()
    serializer_class = GenericoSerializer

    def get_queryset(self, **kwargs):
        try: 
            return self.get_serializer().Meta.model.objects.filter(type=kwargs['type'])
        except: 
            return self.get_serializer().Meta.model.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset(type=kwargs['type']))
        except:
            queryset = self.filter_queryset(self.get_queryset())        

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        type = request.GET.get('type')
        if type is None:
            return self.list(request, *args, **kwargs)
        return self.list(request, type=type)

class CategoriaListAPIView(ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CaterogiaSerializer
    
    # def get(self, request, *args, **kwargs):
    #     print('hola desde get')
    #     return Response({'message': 12}, status=status.HTTP_201_CREATED)

class PreguntaListAPIView(ListAPIView):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

    def get_queryset(self, **kwargs):
        try:
            if kwargs['id']:
                return self.get_serializer().Meta.model.objects.filter(text = kwargs['id'])
        except KeyError as e:
            try:
                if kwargs['key']:
                    id_key = Keyword.objects.get(text=kwargs['key'])
                    preguntas = Pregunta.objects.filter(keyword = id_key)            
                    return self.get_serializer().Meta.model.objects.filter(keyword = id_key)
            except KeyError as e:
                return self.get_serializer().Meta.model.objects.all()
        
        # id_category = Categoria.objects.get(nombre_corto=kwargs['category'])
        # return self.get_serializer().Meta.model.objects.filter(categoria=id_category)

    def list(self, request, *args, **kwargs):
        try:    
            if kwargs['id']:
                queryset = self.filter_queryset(self.get_queryset(id=kwargs['id']))
                print(queryset)
        except KeyError as e:
            try:
                if kwargs['key']:
                    queryset = self.filter_queryset(self.get_queryset(key=kwargs['key']))
            except KeyError as e:
                print(e)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        print(self)
        print(request)
        text_clean = self.get_cleantext(request.data['text'])
        key = self.get_key(text_clean);
        if key is None:
            return Response({'error':'No se encuentra key'}, status=status.HTTP_404_NOT_FOUND)
        # category = request.data['categoria']
        return self.list(request,key=key)

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
        print(list_text)
        new_list = []
        p = re.compile(r'[a-z-áéíóúñ]+')#search only words
        for word in list_text:
            word = ' '.join(p.findall(word)) #example  "mensaje...con" split = "mensaje con"
            word = re.sub(r'([abdefghijkmopqsu-zÀ-ÿ])\1{1,}', r'\1', word)      
            new_list.append(word)
        return new_list

    def get(self, request, *args, **kwargs):
        id_pregunta = request.GET.get('id')
        if id_pregunta is None:
            return self.list(request, *args, **kwargs)
        preguntas = self.list(request, id=id_pregunta)
        if len(preguntas.data) == 0:
            return Response({'error':'No se encuentra key'}, status=status.HTTP_404_NOT_FOUND)
        return self.list(request, id=id_pregunta)


class PreguntaRetrieveAPIView(RetrieveAPIView):
    serializer_class = PreguntaSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()




class GenericoViewSet(viewsets.ModelViewSet):
    queryset = Generico.objects.all()
    serializer_class = GenericoSerializer

    def get_queryset(self,pk=None, **kwargs):
        queryset = super().get_queryset()
        query = self.kwargs
        print(query)
        print(kwargs)
        try:
            queryset = queryset.filter(type = kwargs['type'])
        except KeyError as e:
            if query == {}:
                queryset = queryset.all()
            else:
                queryset = queryset.filter(id = int(query['pk']))
        return queryset
    
    # def list(self,request):        
    #     print(request.GET['type'])
    #     if request.GET['type']:
    #         type = request.GET.get('type')
    #         generico_serializer = self.get_serializer(self.get_queryset(type=type),many = True)
    #     else:
    #         generico_serializer = self.get_serializer(self.get_queryset(),many = True)
    #     return Response(generico_serializer.data, status = status.HTTP_200_OK)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CaterogiaSerializer

class SubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = SubCategoria.objects.all()
    serializer_class = SubcaterogiaSerializer

class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

    def get_queryset(self,pk=None):
        queryset = super().get_queryset()
        query = self.kwargs
        # print(query)
        if query == {}:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(id = int(query['pk']))
        return queryset