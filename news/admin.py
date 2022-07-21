from django.contrib import admin
from django.utils.html import format_html

from .models import News


# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'news_image_tag', 'time_update', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug_news": ('title',)}

    @staticmethod
    def news_image_tag(obj):
        return format_html('<img style="height: 100px;" src="{}" />'.format(obj.photo.url))


admin.site.register(News, NewsAdmin)
