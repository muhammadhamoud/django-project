from django.http import Http404
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime as dt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, generics, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import *  
from homepage.models import *
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class NoPagination(PageNumberPagination):
    page_size = None

class CombinedSiteDataView(APIView):
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        try:
            site_information = SiteInformation.objects.first()
            site_metadata = SiteMetaData.objects.first()
            site_information_additional = SiteInformationAdditional.objects.first()

            if site_information and site_metadata and site_information_additional:
                # Serialize data from each model
                site_information_data = SiteInformationSerializer(site_information).data
                site_metadata_data = SiteMetaDataSerializer(site_metadata).data
                site_information_additional_data = SiteInformationAdditionalSerializer(site_information_additional).data

                # Combine data from all models into a single response
                combined_data = {
                    'site_information': site_information_data,
                    'site_metadata': site_metadata_data,
                    'site_information_additional': site_information_additional_data,
                }

                return Response(combined_data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SiteInformationListView(APIView):
    serializer_class = SiteInformationSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            site_information_objects = SiteInformation.objects.all()
            if site_information_objects:
                serializer = self.serializer_class(site_information_objects, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SiteInformationView(APIView):
    serializer_class = SiteInformationSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            first_object = SiteInformation.objects.first()
            if first_object:
                serializer = self.serializer_class(first_object)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteInformation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SiteMetaDataListView(APIView):
    serializer_class = SiteMetaDataSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            site_metadata_objects = SiteMetaData.objects.all()
            if site_metadata_objects:
                serializer = self.serializer_class(site_metadata_objects, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteMetaData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class SiteInformationAdditionalListView(APIView):
    serializer_class = SiteInformationAdditionalSerializer
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        try:
            site_information_additional_objects = SiteInformationAdditional.objects.all()
            if site_information_additional_objects:
                serializer = self.serializer_class(site_information_additional_objects, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except SiteInformationAdditional.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
  
class CustomModelDataView(generics.ListAPIView):
    # Remove authentication_classes and permission_classes
    authentication_classes = []
    permission_classes = []
    pagination_class = NoPagination

    serializer_class_mapping = {
        'marketing': MarketingSerializer,
        'service': ServiceSerializer,
        'feature': FeatureSerializer,
        'offering': OfferingSerializer,
        'project': ProjectSerializer,
        'teammember': TeammemberSerializer,
        'testimonial': TestimonialSerializer,
        'business_category': BusinessCategorySerializer,
        'framework': FrameworkSerializer,
    }
    def get_serializer_class(self):
        model_name = self.kwargs.get('model_name')
        return self.serializer_class_mapping.get(model_name, None)
    
    def get_queryset(self):
        model_name = self.kwargs.get('model_name')
        if model_name in self.serializer_class_mapping:
            model_class = self.serializer_class_mapping[model_name].Meta.model
            return model_class.objects.all()
        return None

# class AllModelDataView(APIView):
#     def get(self, request, *args, **kwargs):
#         all_data = {}
#         for model_name, serializer_class in CustomModelDataView.serializer_class_mapping.items():
#             queryset = serializer_class.Meta.model.objects.all()
#             serializer = serializer_class(queryset, many=True)
#             all_data[model_name] = serializer.data
#         return Response(all_data)
 
# class AllModelDataView(APIView):
#     def get(self, request, *args, **kwargs):
#         all_data = {}
#         for model_name, serializer_class in CustomModelDataView.serializer_class_mapping.items():
#             queryset = CustomModelDataView.serializer_class_mapping[model_name].Meta.model
#             serializer_class = serializer_class
#             # queryset = serializer_class.Meta.model.objects.all()
#             serializer = serializer_class(queryset, many=True)
#             all_data[model_name] = queryset.objects.all()
#         return Response(all_data)

class AllModelDataView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        all_data = {}
        for model_name, serializer_class in CustomModelDataView.serializer_class_mapping.items():
            # queryset = CustomModelDataView.serializer_class_mapping[model_name].Meta.model.objects.all()
            queryset = CustomModelDataView.serializer_class_mapping[model_name].Meta.model.objects.filter(is_published=True)
            serializer = serializer_class(queryset, many=True, context={'request': request})
            all_data[model_name] = serializer.data
        return Response(all_data)