from django.db import models
from services.languages import LANGUAGES

class Site(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="The name of the site."
    )

    def __str__(self):
        return self.name

class PageName(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='page_names',
        help_text="The site that the page name belongs to."
    )
    name = models.CharField(
        max_length=50,
        help_text="A short name or identifier for the page."
    )

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('site', 'name')

class Page(models.Model):

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='pages',
        help_text="The site that the page belongs to."
    )
    page_name = models.ForeignKey(
        PageName,
        on_delete=models.CASCADE,
        related_name='pages',
        help_text="The name of the page."
    )
    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default='en',
        help_text="The language of the page."
    )
    title = models.CharField(
        max_length=200,
        help_text="The title of the page, up to 200 characters."
    )
    content = models.TextField(
        help_text="The main content of the page."
    )
    description = models.CharField(
        max_length=300,
        blank=True,
        help_text="A brief description or summary of the page."
    )
    image_url = models.URLField(
        blank=True,
        help_text="A URL for an optional image to display with the page."
    )
    icon_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="The name of an optional icon to display with the page."
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Whether the page is currently published and visible to users."
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the page was created."
    )
    date_updated = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the page was last updated."
    )
    slug = models.SlugField(
        unique=False,
         blank=True,
        help_text="A unique URL-friendly identifier for the page. Leave blank to automatically generate from the title."
    )

    def __str__(self):
        return self.title
    
    # class Meta:
    #     unique_together = ('language', 'site', 'page_name', 'title')
    #     # db_table = 'pages_contents'
    #     verbose_name_plural = 'Pages'
    #     ordering = ('-date_updated',)
    #     get_latest_by = 'date_updated'
