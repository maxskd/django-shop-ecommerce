from unittest import TestCase

from .models import OrderItem, Book, Authors, Genres, Countries, Publisher
from .shop_services import ShopService


class ShopTestCase(TestCase):

    def test_strange_action_in_update_quantity(self):
        # If action was anything strange value, update_quantity show error with message that you need to click
        # on the buttons
        res = ShopService.update_quantity('strange', OrderItem.objects.get(pk=1), Book.objects.get(pk=1))
        self.assertEqual(res, 'If you want to change the quantity of an item, just click on the buttons')

    def test_add_action_in_update_quantity(self):
        # If action was add, function check value books and if we can add more books to cart, function add more books
        # in this cart, we can prove them to compare 2 objects, one before call this function, and one after call
        orderItemBefore = OrderItem.objects.get(pk=1)
        res = ShopService.update_quantity('add', OrderItem.objects.get(pk=1), Book.objects.get(pk=1))
        orderItemAfter = OrderItem.objects.get(pk=1)
        self.assertEqual(orderItemBefore.quantity + 1, orderItemAfter.quantity)

    def test_remove_action_in_update_quantity(self):
        # If action was remove, function check value books and if we can remove more to cart, function remove one item
        # in this cart, we can prove them to compare 2 objects, one before call this function, and one after call
        orderItemBefore = OrderItem.objects.get(pk=1)
        res = ShopService.update_quantity('remove', OrderItem.objects.get(pk=1), Book.objects.get(pk=1))
        orderItemAfter = OrderItem.objects.get(pk=1)
        self.assertEqual(orderItemBefore.quantity - 1, orderItemAfter.quantity)

    def test_take_books_by_author(self):
        books, author = ShopService.take_books_by_category('author', 'edgar-allan-poe')
        self.assertEqual(list(books), list(Book.objects.filter(author__slug='edgar-allan-poe').select_related('author',
                                                                                                              'genre')))
        self.assertEqual(author, Authors.get_author(Authors, 'edgar-allan-poe'))

    def test_take_books_by_genre(self):
        books, author = ShopService.take_books_by_category('genre', 'horror')
        self.assertEqual(list(books), list(Book.objects.filter(genre__slug='horror').select_related('author',
                                                                                                    'genre')))
        self.assertEqual(author, Genres.objects.get(slug='horror'))

    def test_take_books_by_country(self):
        books, author = ShopService.take_books_by_category('country', 'germany')
        self.assertEqual(list(books), list(Book.objects.filter(country__slug='germany'). \
                                           select_related('author', 'country', 'genre')))
        self.assertEqual(author, Countries.objects.get(slug='germany'))

    def test_take_books_by_publisher(self):
        books, author = ShopService.take_books_by_category('publisher', 'pearson')
        self.assertEqual(list(books), list(Book.objects.filter(publisher__slug='pearson') \
                                           .select_related('author', 'genre', 'publisher')))
        self.assertEqual(author, Publisher.objects.get(slug='pearson'))

    def test_take_new_books(self):
        books, new = ShopService.take_books_by_category('new', '')
        self.assertEqual(list(books), list(Book.get_new_books(Book, 100)))
        self.assertEqual(new, 'New Arrival in our Shop!')

    def test_take_popular_books(self):
        books, new = ShopService.take_books_by_category('top', '')
        self.assertEqual(list(books), list(Book.get_popular_books(Book, 100)))
        self.assertEqual(new, 'The most popular Books of the World! World Bestsellers and Best Books')

    def test_take_any_books(self):
        books, info = ShopService.take_books_by_category('asdasdasd', '')
        self.assertIs(books, False)
        self.assertIs(info, False)
