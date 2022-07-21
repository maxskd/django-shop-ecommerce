from django.shortcuts import render
from .models import News
from .news_services import NewsService


def news(request):
    posts = NewsService.get_news(7)
    return render(request, 'news/news.html', {'posts': posts})


def show_post(request, post_slug):
    post = NewsService.get_post(post_slug)
    posts = NewsService.get_news(5)
    return render(request, 'news/post.html', {'post': post, 'posts': posts})
