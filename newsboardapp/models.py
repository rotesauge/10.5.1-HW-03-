from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

news = 'NW'
post = 'PO'
TYPE = [
    (news, 'Новость'),
    (post, 'Статья')
]
# Create your models here.
class Author(models.Model):
    id = models.IntegerField(default = 1)
    full_name = models.CharField(max_length=255)
    name = models.CharField(null=True, max_length=64)
    age = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=255, blank=True)
    author = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True, primary_key = True,default = 1
    )
    def update_name(self):
        self.name = self.full_name.split()[0]
        self.save()

    def update_rating(self):
        post_ratings = 0
        for post in Post.objects.filter(author = self):
            post_ratings = post_ratings + post.rating
        comm_ratings = 0
        for comm in Comment.objects.filter(user = self.user):
            comm_ratings = comm_ratings + comm.rating
        comm_ratings2 = 0
        for post in Post.objects.filter(author = self):
            for comm in Comment.objects.filter(post=post):
                comm_ratings2 = comm_ratings2 + comm.rating

        self.rating = post_ratings*3+comm_ratings+comm_ratings2
        self.save()

class Category(models.Model):
    name = models.CharField(null=True, max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name} '

class CensorWords(models.Model):
    name = models.CharField(null=True, max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(null=True, blank=True, default=0)
    caption = models.CharField(null=True, max_length=64)
    text = models.CharField(null=True, max_length=1024)
    datetime = models.DateTimeField(auto_now_add=True)
    сategory = models.ManyToManyField(Category)
    type = models.CharField(max_length=2,
                                choices=TYPE,
                                default=post)

    def __str__(self):
        return f'{self.caption} : {self.text[:20]}'
    def preview(self):
        return self.text[0:124] + '...'

    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating + 1
        self.save()

    def get_absolute_url(self):
        if self.type == 'NW':
            return reverse('post', args=[str(self.id)])
        if self.type == 'PO':
            return reverse('article', args=[str(self.id)])

#class PostCategory(models.Model):
#    post = models.ForeignKey(Post, on_delete=models.CASCADE,default=1)
#   сategory = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, default=1)
    text = models.CharField(null=True, max_length=1024)
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    def like(self):
        self.rating = self.rating + 1
        self.save()

    def dislike(self):
        self.rating = self.rating + 1
        self.save()
