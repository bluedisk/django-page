# -*- coding: utf-8 -*-
import urllib

import re
import os
from django import template
from django.conf import settings

from django.shortcuts import render, get_object_or_404
from django.template import Template, RequestContext, Context
from django.http import Http404, HttpResponse
from django.urls import reverse

from page.models import Page, DownloadableFile, Post, PostCategory

from django.core.exceptions import ObjectDoesNotExist

from page.shortcode import unpack_content_with_request
from page.renderer import render_page, render_post


def home(request):
    try:
        page_obj = Page.objects.get(page_type='root')
    except Page.DoesNotExist:

        try:
            page_obj = Page.objects.get(page_type='main')
        except Page.DoesNotExist:

            try:
                page_obj = Page.objects.get(code='home')
            except Page.DoesNotExist:
                raise Http404()

    return render_page(request, page_obj)


def page(request, page_id=None, page_code=None):
    if not page_id and not page_code:
        raise Http404("Page does not exist")

    page_obj = None

    try:
        if page_id:
            page_obj = Page.objects.get(pk=page_id)

        if page_code:
            page_obj = Page.objects.get(code=page_code)

    except ObjectDoesNotExist:
        raise Http404("Page does not exist")

    if not page_obj:
        raise Http404("Page does not exist")

    return render_page(request, page_obj)


def post(request, post_id):
    if not post_id:
        raise Http404("Page does not exist")

    try:
        post_obj = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post_obj = Post.objects.all().order_by('-created')[0]

    return render_post(request, post_obj)


def post_list(request, cate_id):
    cate = get_object_or_404(PostCategory, code=cate_id)
    posts = Post.objects.filter(active=True, cate=cate)

    default_selected = 0
    if posts:
        default_selected = posts[0].id

    try:
        selected = int(request.GET.get('id', default_selected))
    except ValueError:
        selected = default_selected

    return render(request, 'page/post/list.html', {
        'style_name': 'page/post/style/' + (cate.template or 'basic_list.html'),
        'cate': cate,
        'posts': posts,
        'selected': selected,
    })


def download(request, file_id=None, file_name=None):
    file_obj = get_object_or_404(DownloadableFile, pk=file_id)

    if not file_obj.file:
        raise Http404

    file_name = file_name or os.path.basename(file_obj.file.name)

    response = HttpResponse(file_obj.file, content_type='application/octet-stream')

    filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(file_name.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header

    return response
