from rest_framework import serializers

from homepage.models import (
    SiteInformation, Marketing, Service, Feature, 
    BusinessCategory, Offering, Project, TeamMember, 
    Testimonial, SiteMetaData, SiteInformationAdditional,
    Framework
    )

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

class SiteInformationSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteInformation)
    class Meta:
        model = SiteInformation
        fields = '__all__'

class SiteMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteMetaData
        exclude = ("modified",)

class SiteInformationAdditionalSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SiteInformationAdditional)
    class Meta:
        model = SiteInformationAdditional
        fields = '__all__'

class MarketingSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Marketing)

    class Meta:
        model = Marketing
        fields = '__all__'

class ServiceSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Service)
    class Meta:
        model = Service
        fields = '__all__'

class FeatureSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Feature)
    class Meta:
        model = Feature
        fields = '__all__'

class FrameworkSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Feature)
    class Meta:
        model = Framework
        fields = '__all__'


class BusinessCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BusinessCategory)
    class Meta:
        model = BusinessCategory
        fields = '__all__'

class OfferingSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Offering)
    
    class Meta:
        model = Offering
        exclude = ("modified",)

class ProjectSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Project)
    # category = serializers.SerializerMethodField()
    category = BusinessCategorySerializer(required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def get_category(self, obj):
        return obj.category.name

class TeammemberSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=TeamMember)
    class Meta:
        model = TeamMember
        fields = '__all__'

class TestimonialSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Testimonial)
    class Meta:
        model = Testimonial
        fields = '__all__'


# class CombinedSerializer(TranslatableModelSerializer):
#     marketing = TranslatedFieldsField(shared_model=Marketing)
#     service = TranslatedFieldsField(shared_model=Service)
#     feature = TranslatedFieldsField(shared_model=Feature)
#     business_category = TranslatedFieldsField(shared_model=BusinessCategory)
#     offering = TranslatedFieldsField(shared_model=Offering)
#     project = TranslatedFieldsField(shared_model=Project, fields=('id', 'translations', 'category'))
#     team_member = TranslatedFieldsField(shared_model=TeamMember)
#     testimonial = TranslatedFieldsField(shared_model=Testimonial)

#     class Meta:
#         model = Project  # Choose a model that has all the fields you need
#         fields = '__all__'