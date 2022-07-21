import datetime


from .models import Book, Order, OrderItem, ShippingAddress, Authors, Genres, Countries, Publisher


class ShopService:

    @staticmethod
    def take_books_by_category(category_type, category_slug):
        if category_type == 'author':
            books = Book.objects.filter(author__slug=category_slug).select_related('author', 'genre')
            category_info = Authors.get_author(Authors, category_slug)
            return books, category_info
        elif category_type == 'genre':
            books = Book.objects.filter(genre__slug=category_slug).select_related('author', 'genre')
            category_info = Genres.objects.get(slug=category_slug)
            return books, category_info
        elif category_type == 'country':
            books = Book.objects.filter(country__slug=category_slug).select_related('author', 'country', 'genre')
            category_info = Countries.objects.get(slug=category_slug)
            return books, category_info
        elif category_type == 'publisher':
            books = Book.objects.filter(publisher__slug=category_slug) \
                .select_related('author', 'genre', 'publisher')
            category_info = Publisher.objects.get(slug=category_slug)
            return books, category_info
        elif category_type == 'top':
            books = Book.get_popular_books(Book, 100)
            return books, 'The most popular Books of the World! World Bestsellers and Best Books'
        elif category_type == 'new':
            books = Book.get_new_books(Book, 100)
            return books, 'New Arrival in our Shop!'
        else:
            return False, False

    @staticmethod
    def update_item_in_cart(bookId, customer, action):
        book = Book.objects.get(id=bookId)
        # Check book quality, if we have more than 1 book add or delete. Else - print that this item is out of Stock
        if book.number_of_books >= 1:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(order=order, book=book)
            # Check action, if add - add more item in our orderItem, if remove - remove item
            message = ShopService.update_quantity(action, orderItem, book)
            return message
        else:
            return 'This item is out of Stock'

    @staticmethod
    def update_quantity(action, orderItem, book):
        if action == 'add':
            if orderItem.quantity <= book.number_of_books - 1:
                orderItem.quantity += 1
            else:
                return 'There are no more products, you have chosen the maximum available quantity!'
        elif action == 'remove':
            orderItem.quantity -= 1
        else:
            return 'If you want to change the quantity of an item, just click on the buttons'
        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()
            return 'Item was deleted'

    @staticmethod
    def check_book_quantity_authenticated_user(book, book_quantity, orderItem):
        if book_quantity > 1:
            for b in book:
                for o in orderItem:
                    if b.book == o.book:
                        book_instance = b.book
                        book_instance.number_of_books -= o.quantity
                        book_instance.save()
        elif book_quantity == 1:
            book_instance = book[0].book
            book_instance.number_of_books -= orderItem[0].quantity
            book_instance.save()
        else:
            return False

    @staticmethod
    def process_cart_anonymous_user(cart):
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
                    },
                    'quantity': cart[i]["quantity"]
                }
                items.append(item)
            except ValueError:
                pass
        return items

    @staticmethod
    def check_book_quantity_anonymous_user(items, order):
        book_quantity = 0
        for item in items:
            book = Book.objects.get(id=item['book']['pk'])
            book_quantity += 1
            if book.number_of_books > item['quantity']:
                orderItem = OrderItem.objects.create(book=book, order=order, quantity=item['quantity'])
            else:
                orderItem = OrderItem.objects.create(book=book, order=order, quantity=book.number_of_books)
        allOrderItem = OrderItem.objects.filter(order=order)

        if book_quantity > 1:
            for o in allOrderItem:
                book_instance = o.book
                book_instance.number_of_books -= o.quantity
                book_instance.save()
        elif book_quantity == 1:
            book.number_of_books = book.number_of_books - orderItem.quantity
            book.save()
        else:
            return False

    @staticmethod
    def order_formation(customer, order, data):
        transaction_id = str(round(datetime.datetime.now().timestamp())) + str(order.pk)
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            country=data['shipping']['country'],
            zipcode=data['shipping']['zipcode'],
        )
