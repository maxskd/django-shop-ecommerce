from django.urls import path

from .views import *

urlpatterns = [
    path('', show_shop, name='shop'),
    path('cart/', show_cart, name='cart'),
    path('checkout/', show_checkout, name='checkout'),
    path('process_order/', proces_order, name='process_order'),
    path('update_item/', update_item, name='update_item'),
    path('book/<slug:book_slug>/', show_book, name='book'),
    path('<str:category_type>/<slug:category_slug>/', show_books_by_category, name='category'),
]
