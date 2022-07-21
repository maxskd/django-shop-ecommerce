from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .services import EmailService
from django.contrib.auth import login, logout, authenticate
from shop.models import Order, Customer, OrderItem, Book, Authors
from news.news_services import NewsService


def about(request):
    return render(request, 'main/about.html')


def welcome_page(request):
    authors = Authors.get_authors(Authors, 4)
    news = NewsService.get_news(3)
    books = Book.get_popular_books(Book, 8)
    # Choose any book, just write correct pk
    book_sale = Book.objects.select_related('author', 'genre', 'publisher').get(pk=1)
    return render(request, 'main/welcome.html', {'books': books, 'book_sale': book_sale,
                                                 'news': news, 'authors': authors})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Incorrect Login or Password!')
                return render(request, 'main/login.html')
    return render(request, 'main/login.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                new_user = form.save(commit=False)
                customer = Customer.objects.create(user=new_user)
                messages.success(request,
                                 'Account with name ' + customer.username +
                                 ' successfully created. Now you can login in your account!')
                return redirect('login')
            else:
                messages.error(request, form.errors.as_text())
        else:
            form = CreateUserForm()
    return render(request, 'main/register.html', {'form': form})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


def contact_us(request):
    if request.method == 'POST':
        email_info = EmailService.send_email(subject=request.POST.get('message-subject', ''),
                                             message=request.POST.get('message', ''),
                                             email_sender=request.POST.get('message-email', ''),
                                             )
        messages.success(request, email_info)
        return redirect('contact_us')
    else:
        return render(request, 'main/contact_us.html')


@login_required(login_url='login')
def user_profile(request):
    completed_order = Order.objects.filter(customer=request.user.customer, complete=True).order_by('-date_ordered')

    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, instance=request.user)
        customer_form = CustomerEditForm(data=request.POST, files=request.FILES, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
        else:
            messages.error(request, 'Incorrect value, check your form and try again!')

    else:
        user_form = UserEditForm(instance=request.user)
        customer_form = CustomerEditForm(instance=request.user.customer)

    return render(request, 'main/profile.html',
                  {'user_form': user_form, 'customer_form': customer_form, 'completed_order': completed_order, })
