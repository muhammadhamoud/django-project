# import arrow
from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from parler.models import TranslatableModel, TranslatedFields
from core.models import BaseContent, DRY_TRANSLATION, base_image_path, custom_upload_path_html, custom_upload_path_rm, validate_image_extension
from homepage.models import SiteInformation
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown

# Create your models here.

BLOG_STATUS_CHOICE = (
    ("Drafted", "Drafted"),
    ("Published", "Published"),
    ("Trashed", "Trashed"),
    ("Review", "Review"),
)

ROLE_CHOICE = (
    ("Blog Admin", "blog_admin"),
    ("Blog Publisher", "blog_publisher"),
    ("Blog Author", "blog_author"),
)

class BlogUser(models.Model):
    site = models.ForeignKey(SiteInformation, on_delete=models.CASCADE ,related_name='blog_site')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles"
    )
    role = models.CharField(max_length=200, choices=ROLE_CHOICE, default="blog_author")
    is_active = models.BooleanField(default=True)
	
    class Meta:
        verbose_name_plural = _('Blog Users')

class BlogCategory(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION
    # meta_description = models.TextField(max_length=160, null=True, blank=True)
    # meta_keywords = models.TextField(max_length=255, null=True, blank=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _('Blog Categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(BlogCategory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    def category_posts(self):
        return Post.objects.filter(category=self, status='Published').count()

    def clean(self):
        self.name = (self.name).title()
        super().clean()

class BlogTag(TranslatableModel, BaseContent):
    translations = DRY_TRANSLATION

    class Meta:
        verbose_name_plural = _('Tags')

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            tag = BlogTag.objects.get(pk=self.id)
            if tag.name != self.name:
                self.slug = create_tag_slug(tempslug)
        else:
            self.slug = create_tag_slug(tempslug)
        super(BlogTag, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    def clean(self):
        self.name = str(self.name).title()
        super().clean()

def create_tag_slug(tempslug):
    slugcount = 0
    while True:
        try:
            BlogTag.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + "-" + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug

class Post(TranslatableModel, BaseContent):
    translations = TranslatedFields(
        name=models.CharField(
		max_length=100,
		help_text=_("Enter a name for the content."),
		verbose_name=_("Name"),
		blank=True,
		null=True	
	),
	    description=models.TextField(
		blank=True,
		null=True,
		help_text=_("Enter a description for the content."),
		verbose_name=_("Description")
	),
        file_html = models.FileField(upload_to=custom_upload_path_html, blank=True, null=True),
        file_markdown = models.FileField(upload_to=custom_upload_path_rm, blank=True,  null=True),
        read_time =  models.IntegerField(default=0)
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    tags = models.ManyToManyField(BlogTag, related_name="post")
    status = models.CharField(
        max_length=10, choices=BLOG_STATUS_CHOICE, default="Drafted"
    )
    publish_on = models.DateTimeField(default=timezone.now)
    meta_description = models.TextField(max_length=160, null=True, blank=True)
    meta_keywords = models.TextField(max_length=255, null=True, blank=True)
    meta_author = models.TextField(max_length=255, null=True, blank=True)
    is_page = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('Posts')
        ordering = ('-created',)

    def __str__(self):
        return str(self.name)

    def create_activity(self, user, content):
        return History.objects.create(user=user, post=self, content=content)

    def create_activity_instance(self, user, content):
        return History(user=user, post=self, content=content)

    def get_absolute_url(self):
        return reverse("blog:blog-api:posts-detail", kwargs={"slug": self.slug})

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            post = Post.objects.get(pk=self.id)
            if post.name != self.name:
                self.slug = create_slug(tempslug)
        else:
            self.slug = create_slug(tempslug)

        # Check if status is "Published", if so, set is_published to True
        if self.status == "Published":
            self.is_published = True
        else:
            self.is_published = False

        super(Post, self).save(*args, **kwargs)

        # super().save(*args, **kwargs)


    # @property
    # def created_on_arrow(self):
    #     return arrow.get(self.created_on).humanize()

    # @property
    # def published_on_arrow(self):
    #     return arrow.get(self.publish_on).humanize()


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + "-" + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug


class History(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="history", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_page = models.BooleanField(default=False)

    def __str__(self):
        return "{username} {content} {blog_title}".format(
            username=str(self.user.get_username()),
            content=str(self.content),
            blog_title=str(self.post.name),
        )

    class Meta:
        verbose_name_plural = _('Histories')

class BlogImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    image = models.ImageField(
		upload_to=base_image_path,
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload an image for the articles."),
		verbose_name=_("Image")
	)

    def __str__(self):
        return f"Image of {self.post.name}"

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class FavoritePost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favoritepost"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.post}"

class Like(models.Model):
    like_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text=_("The date and time when the content was created."),
        verbose_name=_("Created")
    )
    modified = models.DateTimeField(
        auto_now=True,
        help_text=_("The date and time when the content was last modified."),
        verbose_name=_("Modified")
    )

    class Meta:
        unique_together = ["like_user", "like_post"]

    def __str__(self):
        return f"{self.like_user} - {self.like_post}"

class Comment(models.Model):
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField(max_length=500)
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text=_("The date and time when the content was created."),
        verbose_name=_("Created")
    )
    modified = models.DateTimeField(
        auto_now=True,
        help_text=_("The date and time when the content was last modified."),
        verbose_name=_("Modified")
    )

    def __str__(self):
        return f"{self.comment_user} - {self.comment_post}"
