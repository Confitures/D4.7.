from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        s = 0
        for r in Post.objects.filter(author=self).values('rating'):  # суммарный рейтинг каждой статьи автора
            s += int(r['rating']) * 3
        for r in Comment.objects.filter(user=self.user).values('rating'):  # суммарный рейтинг всех комментариев автора
            s += int(r['rating'])
        # for c in Post.objects.filter(author=self).values('id'):  # суммарный рейтинг всех комментариев к статьям автора
        #     for r in Comment.objects.filter(id=c.values()).values('rating'):
        #         s += int(r['rating'])
        self.rating = s
        self.save()
        return None


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        # return self.title.title()
        return f'{self.category}'


class Post(models.Model):
    news = 'news'
    article = 'article'
    ITEMS = [
        (news, 'новость'),
        (article, 'статья')
    ]

    title = models.CharField(max_length=264, unique=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    item = models.CharField(max_length=7,
                            choices=ITEMS)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        # return self.title.title()
        return f'{self.title.title()}: {self.text[:20]}...'

    def preview(self):
        return self.text[0:124] + "..."  # ?

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        # return reverse('flatpages/news_detail', args=[str(self.id)])
        return reverse('news_detail', args=[str(self.id)])
        # return reverse('news_create', )
        # return reverse('news', )


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
