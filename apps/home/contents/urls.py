from django.urls import path
from .views import ContentList, get_contents

urlpatterns = [
    path('contents/translations/', ContentList.as_view()),
    path('contents/translations/<str:language>/', get_contents, name='translations_json'),
]