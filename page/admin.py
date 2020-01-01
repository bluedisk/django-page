from django.contrib import admin
from django.core.cache import cache
from reversion.admin import VersionAdmin

from page.models import Page, Pagelet, DownloadableFile, Post, PostCategory, Slide, Popup


class SlideInline(admin.StackedInline):
    sortable = "order"
    model = Slide
    extra = 0

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()


class PopupInline(admin.StackedInline):
    model = Popup
    extra = 0


@admin.register(Page)
class PageAdmin(VersionAdmin):
    list_display = ['title', 'code', 'id', 'page_type_icon', 'updated', 'created']
    inlines = [SlideInline, PopupInline]

    date_hierarchy = 'created'
    fieldsets = (
        (None, {
            'fields': ('code', 'page_type', 'title', 'subtitle', 'featured')
        }),
        ('PC 환경 컨텐츠', {
            'fields': ('content', 'style'),
        }),
        ('모바일 환경 컨텐츠', {
            'classes': ('collapse',),
            'fields': ('mobile_content', 'mobile_style'),
        }),
        ('커스터마이징', {
            'classes': ('collapse',),
            'fields': ('template','script'),
        }),
        ('기록', {
            'fields': ('updated', 'created'),
        }),
    )
    readonly_fields = ('updated', 'created')

    def page_type_icon(self, obj):
        return {
            'root': '루트',
            'main': '메인',
            'home': '루트+메인'
        }.get(obj.page_type, "")


    page_type_icon.readonly=True
    page_type_icon.short_description = "페이지 타입"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()


@admin.register(Pagelet)
class PageletAdmin(VersionAdmin):
    list_display = ['title', 'code', 'id', 'updated', 'created']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()


@admin.register(DownloadableFile)
class DownloadableFileAdmin(VersionAdmin):
    list_display = ['name', 'file', ]
    date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()


@admin.register(Post)
class PostAdmin(VersionAdmin):
    list_display = ['title', 'active', 'topmost', 'created', 'cate']
    list_editable = ['active', 'topmost']
    list_filter = ['cate', 'active', 'topmost']
    date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()
