from django import template
from django.contrib import messages
from django.template import context

from ..models import Order, Book
import json

register = template.Library()


@register.simple_tag
def create_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


@register.simple_tag(takes_context=True)
def load_user_info(context):
    request = context['request']
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all().select_related('book', 'book__author')
        card_items = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = {}
        card_items = 0
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        items = []

        for i in cart:
            try:
                card_items += cart[i]["quantity"]
                book = Book.objects.get(id=i)
                total = (book.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'book': {
                        'pk': book.id,
                        'title': book.title,
                        'price': book.price,
                        'slug_book': book.slug_book,
                        'photo_of_book': book.photo_of_book,
                        'author': book.author,
                    },
                    'quantity': cart[i]["quantity"]
                }
                items.append(item)
                for item in items:
                    book = Book.objects.get(id=item['book']['pk'])
                    if book.number_of_books >= item['quantity']:
                        pass
                    else:
                        gap = int(item['quantity']) - book.number_of_books
                        card_items -= gap
                        item['quantity'] = book.number_of_books
                        messages.error(request, "We haven't this amount of books with name '" + str(book) +
                                       "', you can buy only " + str(book.number_of_books) + " item(s)")
            except ValueError:
                pass

    return {'items': items, 'order': order, 'card_items': card_items, }
