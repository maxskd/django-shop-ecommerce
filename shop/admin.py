from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year_of_published', 'author', 'genre', 'book_image_tag', 'mini_content')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug_book": ('title',)}

    def book_image_tag(self, obj):
        return format_html('<img style="height: 100px;" src="{}" />'.format(obj.photo_of_book.url))


class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'author_image_tag', 'info')
    prepopulated_fields = {"slug": ('name',)}

    def author_image_tag(self, obj):
        return format_html('<img style="height: 100px;" src="{}" />'.format(obj.photo.url))


class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre_image_tag', 'info')
    prepopulated_fields = {"slug": ('name',)}

    def genre_image_tag(self, obj):
        return format_html('<img style="height: 100px;" src="{}" />'.format(obj.photo.url))


class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_image_tag', 'info')
    prepopulated_fields = {"slug": ('name',)}

    def country_image_tag(self, obj):
        return format_html('<img style="height: 100px;" src="{}" />'.format(obj.photo.url))


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'publisher_image_tag', 'info')
    prepopulated_fields = {"slug": ('name',)}

    def publisher_image_tag(self, obj):
        return format_html('<img style="height: 100px;" src="{}" />'.format(obj.photo.url))


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'phone')
    publisher_name = ('user', 'birth_date', 'phone')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'order', 'quantity', 'date_added')


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'country', 'city', 'zipcode', 'date_added')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
