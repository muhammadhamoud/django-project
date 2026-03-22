from django.contrib import admin
from .models import Post, BlogCategory, BlogTag, BlogUser, History, BlogImage, Comment, Like
from parler.admin import TranslatableAdmin, TranslatableTabularInline, TranslatableStackedInline

# Define the get_prepopulated_fields method for all inline classes
def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}

# class BlogAdmin(admin.ModelAdmin):
# 	list_display = ['title','Blogcategory','Blogtags','content']
# 	list_filter=('status','updated_on')
# 	ordering=['publish']

# class BlogCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'description', 'is_active')

# class BlogTagsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')

@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ["name", "status", "is_featured"]
    list_filter = ["status", "is_featured"]
    list_editable = ["status", "is_featured"]
    search_fields = ["translations__name", "translations__description"]
    get_prepopulated_fields = get_prepopulated_fields
    actions = ['publish_posts', 'draft_posts']

    def publish_posts(self, request, queryset):
        queryset.update(status='Published')  

    publish_posts.short_description = "Publish selected posts"


    def draft_posts(self, request, queryset):
        queryset.update(status='Drafted') 

    draft_posts.short_description = "Draft selected posts"


@admin.register(BlogCategory)
class BlogCategoryAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(BlogTag)
class BlogTagAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields


admin.site.register(BlogUser)
admin.site.register(History)
admin.site.register(BlogImage)
admin.site.register(Comment)
admin.site.register(Like)


