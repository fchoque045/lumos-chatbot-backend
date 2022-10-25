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

    def get_response(self, pk=None, **kwargs):
        '''
        Get subcategories by a given Category or subcategories by a given Sucategory or get all if it isn't specified.

        Returns a response
        '''
        queryset = self.get_queryset()
        query = self.kwargs

        if kwargs == {} and query == {}:
            return Response(self.get_serializer(queryset, many=True).data)

        if kwargs != {} and query == {}:
            try:
                query_category = queryset.filter(categoria=kwargs['category'])
                if len(query_category) > 0:
                    return Response(self.get_serializer(query_category, many=True).data)
                else:
                    return Response({'message': f'No se encuentran subcategorias para la categoria con id {kwargs["category"]}'}, status=status.HTTP_404_NOT_FOUND)
            except KeyError as e:
                print(e)

        if kwargs == {}:
            try:
                query_subcategory = queryset.filter(
                    subcategoria=int(query['subcategoria_pk']))
                if len(query_subcategory) > 0:
                    return Response(self.get_serializer(query_subcategory, many=True).data)
                else:
                    return Response({'message': f'No se encuentran subcategorias para la subcategoria con id {query["subcategoria_pk"]}'}, status=status.HTTP_404_NOT_FOUND)
            except:
                return queryset.filter(id=int(query['pk']))

    def list(self, request, *args, **kwargs):
        category = request.GET.get('id_cat')
        if category:
            response = self.filter_queryset(
                self.get_response(category=category))
        else:
            response = self.filter_queryset(self.get_response())
        return response


class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class PreguntaSubcategoriaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSimplifiedSerializer

    def get_queryset(self, pk=None):
        '''
        Get questions by a given Subcategory or get all if it isn't specified.

        Returns a queryset
        '''
        queryset = super().get_queryset()
        query = self.kwargs

        if query == {}:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(
                subcategoria=int(query['subcategoria_pk']))
        return queryset


class PreguntaKeywordViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSimplifiedSerializer

    def get_queryset(self, pk=None, **kwargs):
        '''
        Get questions by a given keyword or get all if it isn't specified.

        Returns a queryset
        '''
        queryset = super().get_queryset()
        try:
            keyword = Keyword.objects.get(text=kwargs['keyword'])
            return Pregunta.objects.filter(keyword=keyword.id)
        except KeyError as e:
            queryset = queryset.all()
        return queryset

    def list(self, request):
        try:
            text_clean = self.get_cleantext(request.GET.get('keyword'))
            keyword = self.get_keyword(text_clean)
            if keyword is None:
                return Response({'message': f'No se encuentra preguntas referidas a la keyword'}, status=status.HTTP_404_NOT_FOUND)
            pregunta_serializer = self.get_serializer(
                self.get_queryset(keyword=keyword), many=True)
            return Response(pregunta_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': f'debe ingresar una keyword como parametro'}, status=status.HTTP_404_NOT_FOUND)

    def get_keyword(self, list_text):
        '''
        Args: list of words [str]

        Returns a word of list if it is found in the Keyword
        '''
        queryset_keywords = list(Keyword.objects.all())
        keywords = [k.text for k in queryset_keywords]
        for word in list_text:
            if word in keywords:
                return word
        return None

    def get_cleantext(self, text):
        '''
        Args: text (str)

        Clean the text and Returns a list of words
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
        return new_list
