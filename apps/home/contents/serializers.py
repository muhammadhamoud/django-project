from rest_framework import serializers
from .models import Page, PageName, Site

class PageNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageName
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            'id',
            'language',
            'title',
            'content',
            'description',
            'image_url',
            'icon_name',
            'is_published',
            'date_created',
            'date_updated',
            'slug',
         ]
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['page_name'] = PageNameSerializer(instance.page_name).data
        rep['site'] = SiteSerializer(instance.site).data
        return rep