from django import template
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from page.shortcode import unpack_content_with_request


def render_page(request, page_obj):
    if request.user_agent.is_mobile and page_obj.mobile_content:
        raw_content = page_obj.mobile_content
    else:
        raw_content = page_obj.content

    content = unpack_content_with_request(request, raw_content, {
        'title': page_obj.title,
        'edit': reverse('admin:page_page_change', args=[page_obj.id])
    })

    template_name = page_obj.template or 'page/page/page.html'

    return render(request, template_name, {
        'page': page_obj,
        'content': content,
        'edit': reverse('admin:page_page_change', args=[page_obj.id]),
        'default_featured': settings.PAGE_FEATURED_DEFAULT if hasattr(settings, "PAGE_FEATURED_DEFAULT") else ''
    })


def render_post(request, post_obj):

    content = unpack_content_with_request(request, post_obj.content)

    return render(request, 'page/post/post.html', {
        'title': post_obj.title,
        'post': post_obj,
        'content': content,
        'cate': post_obj.cate,
        'edit': reverse('admin:page_post_change', args=[post_obj.id]),
        'default_featured': settings.PAGE_FEATURED_DEFAULT if hasattr(settings, "PAGE_FEATURED_DEFAULT") else ''
    })