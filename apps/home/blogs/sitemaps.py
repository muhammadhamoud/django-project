from blogs.models import Post
from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import reverse

def sitemap_xml(request, **kwargs):

    xml = '''<?xml version="1.0" encoding="UTF-8"?>
             <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''

    xml = xml + '<url><loc>' + settings.blogs_DOMAIN + '/</loc></url>'
    pages = Post.objects.filter(is_page=True)
    for page in pages:
        xml = xml + '<url><loc>' + settings.blogs_DOMAIN + \
            reverse('blogs:page_detail', kwargs={
                    'slug': page.slug}) + '</loc></url>'

    blogs = Post.objects.exclude(is_page=True)
    for blog in blogs:
        xml = xml + '<url><loc>' + settings.blogs_DOMAIN + \
            reverse('blogs:blog_detail', kwargs={
                    'slug': blog.slug}) + '</loc></url>'

    xml = xml + '<url><loc>' + settings.blogs_DOMAIN + '/sitemap/</loc></url>'
    xml = xml + '<url><loc>' + settings.blogs_DOMAIN + '/blog/</loc></url>'
    xml = xml + '</urlset>'

    return HttpResponse(xml, content_type="text/xml")
