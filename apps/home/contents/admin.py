from django.contrib import admin

# Register your models here.

from .models import PageName, Page, Site


class PageNameAdmin(admin.ModelAdmin):
    # list_display = ('PageName__site', 'PageName__page_name', 'PageName__title', 'PageName__is_published')
    # list_filter = ('is_published',)
    # exclude = ('summary_html', 'body_html')
    # prepopulated_fields = {"slug": ("title",)}

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'body':
            formfield.widget.attrs.update({
                'rows': 60,
                'style': 'font-family: monospace; width: 810px;',
            })
        return formfield

admin.site.register(PageName, PageNameAdmin)
admin.site.register(Site)
admin.site.register(Page)