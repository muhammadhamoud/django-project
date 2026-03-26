from django import template

register = template.Library()


@register.filter
def get_form_field(form, field_name):
    return form[field_name]


@register.filter
def get_item(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)


@register.filter
def widget_classname(bound_field):
    return bound_field.field.widget.__class__.__name__