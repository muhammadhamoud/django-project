from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import filters
from django.utils.text import slugify
from django.db.models import Q

from blogs.models import *
from .serializers import *

from rest_framework.pagination import PageNumberPagination
class NoPagination(PageNumberPagination):
    page_size = None

class PaginationFifty(PageNumberPagination):
    page_size = 50

class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.filter(post__isnull=False, post__status='Published').distinct()
    serializer_class = BlogCategorySerializer
    pagination_class = NoPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BlogTagListView(generics.ListAPIView):
    queryset = BlogTag.objects.filter(post__isnull=False, post__status='Published').distinct()
    serializer_class = BlogTagSerializer
    pagination_class = NoPagination

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(status='Published')
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')  # Get the slug from URL
        queryset = queryset.filter(Q(slug__icontains=slug))
        return queryset


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields  = ['translations__name']

    def get_queryset(self):
        queryset = Post.objects.filter(status='Published').distinct()
        is_page = self.request.query_params.get('is_page', None)
        is_featured = self.request.query_params.get('is_featured', None)
        category = self.request.query_params.get('category', None)
        tag = self.request.query_params.get('tag', None)
        # search_term = self.request.query_params.get('search', None)
        slug = self.request.query_params.get('slug', None)
        
        if slug is not None:
            queryset = queryset.filter(slug=slug)

        if is_page is not None:
            queryset = queryset.filter(is_page=is_page)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured)
        if category:
            queryset = queryset.filter(category__slug=category)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        # if search_term:
        #     queryset = queryset.filter(Q(translations__name__icontains=search_term))
        return queryset


class PostNameListView(generics.ListAPIView):
    serializer_class = PostNameListSerializer
    pagination_class = PaginationFifty
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filterset_fields = ['translations__name']
    search_fields  = ['translations__name'] #, 'translations__description'

    def get_queryset(self):
        queryset = Post.objects.filter(status='Published').distinct()
        is_page = self.request.query_params.get('is_page', None)
        is_featured = self.request.query_params.get('is_featured', None)
        category = self.request.query_params.get('category', None)
        tag = self.request.query_params.get('tag', None)
        search_term = self.request.query_params.get('search', None)
        slug = self.request.query_params.get('slug', None)
        
        if slug is not None:
            queryset = queryset.filter(slug=slug)

        if is_page is not None:
            queryset = queryset.filter(is_page=is_page)
        if is_featured is not None:
            queryset = queryset.filter(is_featured=is_featured)
        if category:
            queryset = queryset.filter(category__slug=category)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # print(search_term)
        # if search_term:
        #     queryset = queryset.filter(translations__name__icontains=search_term)

            # all_queries = None
            # search_fields = []
            # for keyword in search_term.split(' '):
            #     keyword_query = None
            #     for field in search_fields:
            #         each_query = Q(**{field+'__icontains':keyword})
            #         if not keyword_query:
            #             keyword_query = each_query
            #         else:
            #             keyword_query = keyword_query | each_query
            #     if not all_queries:
            #         all_queries = keyword_query
            #     else:
            #         all_queries = all_queries & keyword_query
            #         queryset = queryset.filter(all_queries).distinct()
        
        return queryset


# class PostNameListSearchView(generics.ListAPIView):
#     queryset = Post.objects.filter(status='Published').distinct()
#     serializer_class = PostNameListSerializer
#     pagination_class = PaginationFifty
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     search_fields  = ['translations__name', 'translations_description']





# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_published=True, status='Published').distinct()
#     serializer_class = PostSerializer

#     filter_backends = (
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     )
    
#     # def list(self, request, *args, **kwargs):
#     #     queryset = self.get_queryset()
#     #     serializer = self.get_serializer(queryset, many=True)
#     #     return Response(serializer.data)

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         id = self.request.query_params.get('id')
#         category = self.request.query_params.get('category')
#         tag = self.request.query_params.get('tag')
#         search_term = self.request.query_params.get('search')

#         if category:
#             queryset = queryset.filter(category__slug=category)
#         elif tag:
#             queryset = queryset.filter(tags__slug=tag)
        
#         elif id:
#             queryset = queryset.filter(id=id)
       
#         elif search_term:
#             queryset = queryset.filter(Q(translations__name__icontains=search_term))

#         return queryset


# class PageListView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_published=True, status='Published', is_page=True).distinct()
#     serializer_class = PostSerializer

#     filter_backends = (
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     )

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         id = self.request.query_params.get('id')
#         category = self.request.query_params.get('category')
#         tag = self.request.query_params.get('tag')
#         search_term = self.request.query_params.get('search')

#         if category:
#             queryset = queryset.filter(category__slug=category)
#         elif tag:
#             queryset = queryset.filter(tags__slug=tag)
        
#         elif id:
#             queryset = queryset.filter(id=id)
       
#         elif search_term:
#             queryset = queryset.filter(Q(translations__name__icontains=search_term))

#         return queryset


# class FeaturedListView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_published=True, status='Published', is_page=True, is_featured=True).distinct()
#     serializer_class = PostSerializer

#     filter_backends = (
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     )

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         id = self.request.query_params.get('id')
#         category = self.request.query_params.get('category')
#         tag = self.request.query_params.get('tag')
#         search_term = self.request.query_params.get('search')

#         if category:
#             queryset = queryset.filter(category__slug=category)
#         elif tag:
#             queryset = queryset.filter(tags__slug=tag)
        
#         elif id:
#             queryset = queryset.filter(id=id)
       
#         elif search_term:
#             queryset = queryset.filter(Q(translations__name__icontains=search_term))

#         return queryset
