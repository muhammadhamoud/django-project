from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Page
# Create your views here.
from .serializers import ContentsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request

class ContentList(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    serializer_class = ContentsSerializer


@csrf_exempt
def get_contents(request, language):
    if request.method == 'GET':
        content = Page.objects.filter(language=language)
        contents_serializer = ContentsSerializer(content,many=True)
        # print(contents_serializer.data)
        return JsonResponse(contents_serializer.data, safe=False)


# def translations_json_details(request):

#     #Get all
#     language= 'en'
#     if request.method == 'GET':
#         translations = Page.objects.all()
#         translations_serializer = PageSerializer(translations,many=True)
#         print(translations_serializer.data)
#         return JsonResponse(translations_serializer.data, safe=False)


    # # Get all translations for the specified language
    # translations = Page.objects.filter(language=language)

    # # Serialize the translations to JSON
    # json_translations = serializers.serialize('json', translations)

    # # Return the JSON data as a response
    # return JsonResponse(json_translations, safe=False)

# # Get all translations for a specific language
# translations = Page.objects.filter(language='en')

# # Serialize the translations to JSON
# json_translations = serializers.serialize('json', translations)

# # Output the JSON data
# print(json_translations)

