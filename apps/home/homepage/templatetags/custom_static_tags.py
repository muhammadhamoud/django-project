from django import template

register = template.Library()

js_scripts = ['403.js', '492.js', '915.js']

@register.simple_tag
def include_js_scripts():
    script_tags = ""
    for js_script in js_scripts:
        script_tags += f'<script src="{{% static "{js_script}" %}}" type="module"></script>\n'
    return script_tags