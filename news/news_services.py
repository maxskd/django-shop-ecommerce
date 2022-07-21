from .models import News


class NewsService:

    @staticmethod
    def get_news(limit: int):
        return News.objects.all().order_by('-time_update').only('title', 'mini_content', 'time_update',
                                                                'photo', 'slug_news')[:limit]

    @staticmethod
    def get_post(post_slug):
        return News.objects.get(slug_news=post_slug)
