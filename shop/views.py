import datetime
import json
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .filters import *
from .models import Book, Order, OrderItem
from .shop_services import ShopService
from django.contrib.auth.models import User


def show_shop(request):
    books = Book.get_popular_books(Book, 8)
    new_books = Book.get_new_books(Book, 8)
    return render(request, 'shop/shop.html', {'books': books, 'new_books': new_books})


def show_book(request, book_slug):
    book = Book.get_book(Book, book_slug)
    return render(request, 'shop/book.html', {'book': book})


def show_cart(request):
    return render(request, 'shop/cart.html')


def show_books_by_category(request, category_type, category_slug):
    # Check category type, then take all by our category
    books, info_about_category = ShopService.take_books_by_category(category_type, category_slug)
    # Search in Title Filter
    title_contains_query = request.GET.get('title-contains')
    if title_contains_query != '' and title_contains_query is not None:
        books = books.filter(title__icontains=title_contains_query)
    # Another Filters (by Author, by Genre, by Country, by Publisher)
    type_filter = category_type
    books_filter = BookFilter(request.GET, queryset=books)
    books = books_filter.qs
    # Pagination
    paginator = Paginator(books, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/category.html',
                  {'books': page_obj, 'type_filter': type_filter, 'info_about_category': info_about_category,
                   'page_obj': page_obj, 'books_filter': books_filter, })


def update_item(request):
    # Grab all information
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    customer = request.user.customer
    inf = ShopService.update_item_in_cart(bookId, customer, action)
    messages.error(request, inf)
    return JsonResponse('', safe=False)


def show_checkout(request):
    return render(request, 'shop/checkout.html')


def proces_order(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        book = order.orderitem_set.all()
        orderItem = OrderItem.objects.filter(order=order)
        ShopService.check_book_quantity_authenticated_user(book, book.count(), orderItem)
    else:
        name = data['form']['name']
        email = data['form']['email']

        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = {}

        user, created = User.objects.get_or_create(username=name, email=email)
        user.save()
        customer, created = Customer.objects.get_or_create(user=user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = ShopService.process_cart_anonymous_user(cart)
        ShopService.check_book_quantity_anonymous_user(items, order)

    ShopService.order_formation(customer, order, data)

    return JsonResponse('Payment completed', safe=False)
