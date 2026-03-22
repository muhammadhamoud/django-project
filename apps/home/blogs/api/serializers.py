from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from blogs.models import BlogCategory, Comment, Post, FavoritePost, BlogTag, BlogImage

User = get_user_model()

class BlogCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=BlogCategory)
    category_posts = serializers.SerializerMethodField()
    class Meta:
        model = BlogCategory
        exclude = (
            "is_featured",
            "is_published",
            "created",
            "modified",
       )

    def get_category_posts(self, obj):
        return obj.category_posts()

class BlogTagSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=BlogTag)
    class Meta:
        model = BlogTag
        # fields = '__all__'
        exclude = (
            "is_featured",
            "is_published",
            "created",
            "modified",
       )

class CommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.StringRelatedField()
    comment_post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        # fields = ["id", "comment_user", "comment_post", "comment", "created_at"]
        fields = "__all__"
        read_only_fields = ["created_at"]

class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'image_url']
        read_only_fields = ['id', 'image_url']

    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        return obj.image_url



    # post = serializers.StringRelatedField() 

    # class Meta:
    #     model = BlogImage
    #     fields = '__all__'
    #     read_only_fields = ['id', 'image']

    # image_url = serializers.SerializerMethodField()

    # def get_image_url(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         if request is not None:
    #             return request.build_absolute_uri(obj.image.url)
    #         else:
    #             return obj.image.url
    #     return None


class PostSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Post)
    author = serializers.SerializerMethodField()
    likes = serializers.IntegerField(read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)
    category = BlogCategorySerializer()
    tags = BlogTagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # images = BlogImageSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = "__all__"

    def get_author(self, obj):
        return obj.author.get_full_name() if obj.author else None

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if obj:
            return request.build_absolute_uri(obj.slug)

    # def get_images(self, obj):
    #     # Get the related images for the post
    #     images = obj.post_images.all()
    #     if images.exists():
    #         # Serialize the images using BlogImageSerializer
    #         serializer = BlogImageSerializer(images, many=True)
    #         return serializer.data
    #     else:
    #         # If no images exist, return an empty list
    #         return []

    def get_images(self, obj):
        # Get the related images for the post
        images = obj.post_images.all()
        if images.exists():
            request = self.context.get('request')
            if request is not None:
                # Construct full URLs for the images
                return [request.build_absolute_uri(image.image.url) for image in images]
        return []


class BlogCategoryTranslationSerializer(TranslatableModelSerializer):
    id = serializers.IntegerField()
    translations = TranslatedFieldsField(shared_model=BlogCategory)

    class Meta:
        model = BlogCategory
        fields = ['id', 'translations']

class PostNameListSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Post)
    absolute_url = serializers.SerializerMethodField(read_only=True)
    category = BlogCategoryTranslationSerializer()

    class Meta:
        model = Post
        # fields = "__all__"
        exclude = ("icon", "is_featured", "modified", "status", "publish_on", "meta_description", "meta_keywords", "meta_author", "author", "tags")

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if obj:
            return request.build_absolute_uri(obj.slug)



# class PostSerializers(serializers.ModelSerializer):
#     likes = serializers.IntegerField(read_only=True)
#     absolute_url = serializers.SerializerMethodField(read_only=True)
#     author = serializers.SlugRelatedField(slug_field="full_name", read_only=True)
#     category = serializers.SlugRelatedField(
#         queryset=BlogCategory.objects.all(),
#         slug_field="id",
#     )

#     comments = CommentSerializer(many=True, read_only=True)
    

#     def get_absolute_url(self, obj):
#         request = self.context.get("request")
#         if obj:
#             return request.build_absolute_uri(obj.slug)

#     def to_representation(self, instance):

#         rep = super().to_representation(instance)
#         request = self.context.get("request")

#         if request.parser_context.get("kwargs").get("slug"):
#             rep.pop("absolute_url", None)
#         else:
#             rep.pop("content", None)
#             rep.pop("comments", None)

#         rep["category"] = BlogCategorySerializer(instance.category).data["name"]

#         return rep

#     class Meta:
#         model = Post
#         fields = "__all__"
#         # fields = [
#         #     "id",
#         #     "author",
#         #     "category",
#         #     "title",
#         #     "slug",
#         #     "content",
#         #     "status",
#         #     "image",
#         #     "likes",
#         #     "comments",
#         #     "absolute_url",
#         #     "created_at",
#         #     "updated_at",
#         #     "published_at",
#         # ]
#         # read_only_fields = ["slug"]


class FilterSerializer(serializers.Serializer):
    """
    These fields are used in the filters.py
    """
    name = serializers.CharField(required=False, max_length=100)
    search = serializers.CharField(required=False, max_length=100)
    author__in = serializers.CharField(required=False, max_length=100)
    category__name = serializers.CharField(required=False, max_length=100)
    created_at__range = serializers.CharField(required=False, max_length=100)


class SimplePostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(read_only=True)
    absolute_url = serializers.SerializerMethodField(read_only=True)

    author = serializers.SlugRelatedField(slug_field="full_name", read_only=True)

    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if obj:
            return request.build_absolute_uri(
                reverse("blog:api-v1:posts-detail", args=[obj.slug])
            )

    class Meta:
        model = Post
        # fields = [
        #     "id",
        #     "author",
        #     "category",
        #     "title",
        #     "likes",
        #     "absolute_url",
        # ]
        read_only_fields = ["absolute_url"]


class FavoritePostSerializer(serializers.ModelSerializer):
    post = SimplePostSerializer(read_only=True)

    class Meta:
        model = FavoritePost
        fields = ["id", "post"]









# from rest_framework import serializers
# from blogs.models import BlogUser, BlogCategory, BlogTag, Article, History

# class BlogUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogUser
#         fields = ['id', 'user', 'role', 'is_active']

# class BlogCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogCategory
#         fields = '__all__'

# class BlogTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogTag
#         fields = '__all__'

# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'

# class HistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = History
#         fields = '__all__'