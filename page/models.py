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

    SPECIAL_CHOICES = (
        (None, '일반 페이지'),
        ('root', '루트 페이지'),
        ('main', '메인 페이지'),
        ('home', '루트 + 메인')
    )

    code = models.SlugField('페이지 코드', unique=True, help_text='페이지 url로 사용됩니다. 단, "home"의 경우 예외적으로 루트가 됩니다.')
    page_type = models.CharField('특별한 페이지', null=True, choices=SPECIAL_CHOICES, default=None, max_length=10,
                               help_text="""
    랜딩 페이지: 처음 사이트에 진입하면 표시되는 사이트 입니다. 페이지 코드와 무관하게 루트 주소 "/"를 갖습니다.<br/>
    메인 페이지: 페이지 내에서 첫 페이지로 돌아갈 때에 목적지가 되는 페이지 입니다. 로고나 '처음으로' 버튼 등에 링크됩니다.<br/>
    랜딩 + 메인: 루트이자 첫 페이지로 대부분의 사이트에서 홈페이지에 해당 됩니다.
    """)

    title = models.CharField('페이지 제목', max_length=40)
    subtitle = models.CharField('페이지 부제목(선택)', max_length=100, blank=True, null=True)
    featured = ThumbnailerImageField('타이틀 이미지', upload_to='featured',
                                     blank=True, null=True, help_text='이미지 추가 시 페이지 상단에 이미지 타이틀이 표시 됩니다.')

    content = RichTextUploadingField('PC 페이지 내용', config_name='page')
    style = models.TextField('CSS', default='', blank=True, null=True, help_text='스타일 시트에 추가할 내용(테그 없이 작성)')

    mobile_content = RichTextUploadingField('모바일 페이지 내용', config_name='page', blank=True, null=True)
    mobile_style = models.TextField('CSS', default='', blank=True, null=True, help_text='스타일 시트에 추가할 내용(테그 없이 작성)')

    script = models.TextField('Script', default='', blank=True, null=True, help_text='페이지에 추가할 스크립트 내용(테그 없이 작성)')
    template = models.CharField('커스텀 템플릿', max_length=256, default='', blank=True,
                                null=True, help_text='사이트 기본 템플릿(page.html)을 사용하지 않고 별도 템플릿을 사용하려는 경우 지정')

    updated = models.DateTimeField('업데이트', auto_now=True)
    created = models.DateTimeField('생성일', auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.page_type == 'main':
            if Page.objects.filter(page_type='main').exists():
                Page.objects.filter(page_type='main').update(page_type=None)

            if Page.objects.filter(page_type='home').exists():
                Page.objects.filter(page_type='home').update(page_type='root')

        elif self.page_type == 'root':
            if Page.objects.filter(page_type__in=['home', 'root']).exists():
                if Page.objects.filter(page_type='main').exists():
                    Page.objects.filter(page_type='main').update(page_type=None)
                Page.objects.filter(page_type__in=['home', 'root']).update(page_type='main')

        elif self.page_type == 'home':
            Page.objects.update(page_type=None)

        super().save(force_insert, force_update, using, update_fields)


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

    def get_delay_as_msec(self):
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

    content = RichTextUploadingField('문구 내용', config_name='pagelet', null=True, blank=True, default="")

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

    cate = models.ForeignKey(PostCategory, on_delete=models.CASCADE)

    topmost = models.BooleanField("상단고정", default=False, help_text='선택 시 리스트 상단에 고정 됩니다.')
    active = models.BooleanField('표시여부', default=True, help_text='체크 되어 있을 때 리스트에 표시 됩니다')
    featured = ThumbnailerImageField('타이틀 이미지', upload_to='featured',
                                     blank=True, null=True, help_text='이미지 추가 시 페이지 상단에 이미지 타이틀이 표시 됩니다.')

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


class Popup(models.Model):
    class Meta:
        verbose_name = "팝업창"
        verbose_name_plural = "팝업창 목록"

    def __str__(self):
        return self.title

    title = models.CharField('제목', max_length=300, help_text='관리자 구분용이고 외부에 표출되지 않습니다.')
    page = models.ForeignKey(Page, verbose_name='표출 할 페이지', on_delete=models.CASCADE)

    is_active = models.BooleanField('활성화 여부', default=False)

    pos_x = models.CharField('팝업 가로 위치', max_length=100, default='50px')
    pos_y = models.CharField('팝업 세로 위치', max_length=100, default='150px')

    content = RichTextUploadingField('팝업 내용', config_name='post', help_text='팝업 내용을 직접 작성하는 경우 입력', blank=True,
                                     null=True)
    image = models.ImageField('풀 이미지 팝업', upload_to='popup', blank=True, null=True,
                              help_text='설정시 전체 팝업 내용은 이미지로만 채워집니다.')

    created = models.DateTimeField('생성일', auto_now_add=True)
