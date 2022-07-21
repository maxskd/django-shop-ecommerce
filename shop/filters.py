import django_filters
from django import forms
from django_filters import *

from .models import *


class BookFilter(django_filters.FilterSet):
    CHOISES = (
        ('ascending-price', 'Sort by price: low to high'),
        ('descending-price', 'Sort by price: high to low'),
        ('date', 'Sort by latest'),
        ('popularity', 'Sort by popularity')
    )

    title = CharFilter(lookup_expr='icontains', widget=forms.TextInput(attrs={'class': "form-control form-filter"}))
    author = ModelChoiceFilter(queryset=Authors.objects.all(),
                               widget=forms.Select(attrs={'class': "form-control form-filter"}))
    genre = ModelChoiceFilter(queryset=Genres.objects.all(),
                              widget=forms.Select(attrs={'class': "form-control form-filter"}))
    country = ModelChoiceFilter(queryset=Countries.objects.all(),
                                widget=forms.Select(attrs={'class': "form-control form-filter"}))
    publisher = ModelChoiceFilter(queryset=Publisher.objects.all(),
                                  widget=forms.Select(attrs={'class': "form-control form-filter"}))
    ordering = ChoiceFilter(label='Ordering', choices=CHOISES, method='filter_by_order')

    class Meta:
        model = Book
        fields = ('author', 'genre', 'country', 'publisher')

    @staticmethod
    def filter_by_order(queryset, name, value):
        if value == 'ascending-price':
            expression = 'price'
        elif value == 'descending-price':
            expression = '-price'
        elif value == '-date':
            expression = 'year_of_published'
        else:
            expression = '-number_of_books'
        return queryset.order_by(expression)
