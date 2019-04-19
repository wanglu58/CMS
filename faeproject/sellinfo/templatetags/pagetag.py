from django import template

register = template.Library()

from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page,loop_page):
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<span class="current" href="?page=%s">%s</span>'%(loop_page,loop_page)
        else:
            page_ele = '<a class="num" href="?page=%s">%s</a>'%(loop_page,loop_page)
        return format_html(page_ele)
    else:
        return ''

@register.simple_tag
def circle_pages(curr_page,loop_page,name,times):
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<span class="current" href="?name=%s&times=%s&page=%s">%s</span>'%(name,times,loop_page,loop_page)
        else:
            page_ele = '<a class="num" href="?name=%s&times=%s&page=%s">%s</a>'%(name,times,loop_page,loop_page)
        return format_html(page_ele)
    else:
        return ''

@register.simple_tag
def circle_pagess(curr_page,loop_page,name):
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<span class="current" href="?name=%s&page=%s">%s</span>'%(name,loop_page,loop_page)
        else:
            page_ele = '<a class="num" href="?name=%s&page=%s">%s</a>'%(name,loop_page,loop_page)
        return format_html(page_ele)
    else:
        return ''