from django import template
from django.utils.safestring import mark_safe

from shop.models import Category

register = template.Library()


@register.simple_tag
def categories():
    items = Category.objects.all()
    items_li = ""
    for i in items:
        items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.name, i.description)
    return mark_safe(items_li)


@register.simple_tag
def categories_li_a():
    items = Category.objects.all()
    items_li_a = ""
    for i in items:
        list_item = ""
        if i.parent == None :
            parent_item=""
            for value in i.category_set.all():
                parent_item +="""<li class="p-t-4"><a href="/category/{}" class="s-text13">{}</a></li>""".format(value.id, value.description)
            list_item = """ <li >
                                <a href="#{}" data-toggle="collapse" aria-expanded="false" aria-controls="{}" class="dropdown-toggle p-t-4">{}</a>
                                <ul class="collapse" id="{}">
                                    {}
                                </ul>
                            </li>
                        """.format(i.name, i.name, i.name, i.name, mark_safe(parent_item))
        items_li_a += mark_safe(list_item) 
    return mark_safe(items_li_a)


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url
