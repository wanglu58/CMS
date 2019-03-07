__Author = 'Kongzhagen'

from django import template

register = template.Library()

from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page,loop_page):
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<span class="external current" href="?page=%s">%s</span>'%(loop_page,loop_page)
            # page_ele = '<span class="current"><strong>%s</strong></span>'%(loop_page)
        else:
            page_ele = '<a class="external num" href="?page=%s">%s</a>'%(loop_page,loop_page)
            # page_ele = '<span class="num">%s</span>'%(loop_page)
        return format_html(page_ele)
    else:
        return ''