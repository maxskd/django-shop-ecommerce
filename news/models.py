from django.db import models

# Create your models here.
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=100)
    slug_news = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    mini_content = models.CharField(max_length=100, null=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug_news})

    class Meta:
        verbose_name_plural = 'Blog News'
        ordering = ['-time_update', 'title']
