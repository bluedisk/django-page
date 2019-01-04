# -*- coding: utf-8 -*-
import os
from uuid import uuid4

from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from easy_thumbnails.fields import ThumbnailerImageField


class Page(models.Model):
    class Meta:
        verbose_name = "페이지"
        verbose_name_plural = "페이지 목록"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/" % self.code

    code = models.SlugField('페이지 코드', unique=True)
    title = models.CharField('페이지 제목', max_length=40)
    subtitle = models.CharField('페이지 부제목(선택)', max_length=100, blank=True, null=True)
    featured = ThumbnailerImageField('타이틀 이미지', upload_to='featured',
                                     blank=True, null=True, help_text='이미지 추가 시 페이지 상단에 이미지 타이틀이 표시 됩니다.')

    content = RichTextUploadingField('페이지 내용', config_name='page')
    style = models.TextField('Style', default='', blank=True, null=True)
    script = models.TextField('Script', default='', blank=True, null=True)

    updated = models.DateTimeField('업데이트', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)


def path_and_rename(instance, filename):
    prefix = "slide"
    ext = filename.split('.')[-1]
    page = "pid_%s" % (instance.page.id,)
    # get filename
    if instance.pk:
        complaint_id = "cid_%s" % (instance.pk,)
        filename = '{}.{}.{}.{}'.format(prefix, page, complaint_id, ext)
    else:
        # set filename as random string
        random_id = "rid_%s" % (uuid4().hex,)
        filename = '{}.{}.{}.{}'.format(prefix, page, random_id, ext)

        # return the whole path to the file
    return os.path.join("slide", filename)


class Slide(models.Model):
    class Meta:
        verbose_name = "슬라이드"
        verbose_name_plural = "슬라이드"
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_delay_as_second(self):
        return self.delay * 1000

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='slides')
    order = models.PositiveIntegerField('슬라이드 순서', default=0, db_index=True)

    image = ThumbnailerImageField(help_text='슬라이드 이미지', upload_to=path_and_rename)

    title = models.CharField('제목', max_length=40, blank=True, default="")
    subtitle = models.CharField('부제목', max_length=100, blank=True, default="")
    description = models.TextField('추가설명', null=True, blank=True)

    delay = models.PositiveIntegerField('표시시간', default=12, help_text='슬라이드가 표시되는 시간(초)')

    button_label = models.CharField('버튼 이름 제목', max_length=40, blank=True, null=True, help_text='공백인 경우 버튼이 표시 되지 않음')
    button_link = models.URLField('버튼 링크', blank=True, null=True)


class Pagelet(models.Model):
    class Meta:
        verbose_name = "반복사용문구"
        verbose_name_plural = "반복사용문구 목록"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/" % self.code

    title = models.CharField('문구 제목', max_length=40)
    code = models.SlugField('문구 코드', unique=True)

    content = RichTextUploadingField('문구 내용', config_name='pagelet')

    updated = models.DateTimeField('업데이트', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)


class PostCategory(models.Model):
    class Meta:
        verbose_name = "포스트 카테고리"
        verbose_name_plural = "포스트 카테고리 목록"

    def __str__(self):
        return self.name

    code = models.CharField('카테고리 코드', max_length=10, primary_key=True)
    name = models.CharField('카테고리 제목', max_length=40)
    desc = models.CharField('카테고리 한줄 설명', max_length=80)
    link = models.CharField('키테고리 페이지 링크', max_length=1024, null=True, blank=True)

    template = models.CharField('특수 템플릿',
                                max_length=80,
                                default=None,
                                null=True,
                                blank=True,
                                help_text="이 카테고리가 특수한 템플릿을 쓸 경우 템플릿명"
                                )


class Post(models.Model):
    class Meta:
        verbose_name = "포스트"
        verbose_name_plural = "포스트 목록"

        ordering = ['-topmost', '-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.cate.code == 'faq':
            return "/prepare/#faq-%s" % self.pk

        return reverse("page:post", args=[self.id])

    cate = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.CASCADE)

    topmost = models.BooleanField("상단고정", default=False, help_text='선택 시 리스트 상단에 고정 됩니다.')
    active = models.BooleanField('표시여부', default=True, help_text='체크 되어 있을 때 리스트에 표시 됩니다')

    title = models.CharField('포스트 제목', max_length=40)
    content = RichTextUploadingField('포스트 내용', config_name='post')
    summary = models.TextField('요약 내용')

    updated = models.DateTimeField('업데이트', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)


class DownloadableFile(models.Model):

    class Meta:
        verbose_name = "다운로드용 파일"
        verbose_name_plural = "다운로드용 파일 목록"

    def __str__(self):
        return self.name or "-"

    name = models.CharField('표시 할 파일명', max_length=40)
    file = models.FileField('양식 파일', upload_to="forms", null=True, blank=True)

    created = models.DateField('생성일자', auto_now_add=True)
