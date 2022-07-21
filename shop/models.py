from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_user = models.ImageField(upload_to="photos_user/%Y/%m/%d/")
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = 'Customers'


class Book(models.Model):
    title = models.CharField(max_length=100)
    mini_content = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    slug_book = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.ForeignKey('Authors', on_delete=models.PROTECT, null=True, default=None)
    genre = models.ForeignKey('Genres', on_delete=models.PROTECT, null=True, default=None)
    country = models.ForeignKey('Countries', on_delete=models.PROTECT, null=True, default=None)
    year_of_published = models.DateTimeField()
    content = models.TextField(blank=True)
    publisher = models.ForeignKey('Publisher', on_delete=models.PROTECT, null=True, default=None)
    number_of_pages = models.IntegerField()
    number_of_books = models.IntegerField()
    photo_of_book = models.ImageField(upload_to="books_photos/%Y/%m/%d/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Books'

    def get_new_books(self, limit):
        return self.objects.all().select_related('author', 'genre', 'publisher').order_by('-year_of_published')[:limit]

    def get_popular_books(self, limit):
        return self.objects.all().select_related('author', 'genre', 'publisher').order_by('-number_of_books')[:limit]

    def get_book(self, slug):
        return self.objects.select_related('author', 'genre', 'country', 'publisher').get(slug_book=slug)


class Authors(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="author_photos/%Y/%m/%d/")
    info = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'

    def get_authors(self, limit):
        return self.objects.all()[:limit]

    def get_author(self, slug):
        return self.objects.get(slug=slug)


class Genres(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="genre_photos/%Y/%m/%d/")
    info = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Genres'


class Countries(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="country_photos/%Y/%m/%d/")
    info = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Countries'


class Publisher(models.Model):
    name = models.CharField(max_length=75)
    photo = models.ImageField(upload_to="publisher_photos/%Y/%m/%d/")
    year = models.IntegerField()
    info = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Publishers'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.pk)

    @property
    def get_cart_total(self):
        orderItems = self.orderitem_set.prefetch_related('book')
        total = sum([item.get_total() for item in orderItems])
        return total

    @property
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

    @property
    def parts_with_books(self):
        return self.orderitem_set.all().select_related('book')


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        total = self.book.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name_plural = 'Shipping Addresses'
