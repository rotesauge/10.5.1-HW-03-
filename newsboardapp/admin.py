from django.contrib import admin
from .models import Category, Post,Author,CensorWords,Comment
# Register your models here.



admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(CensorWords)
admin.site.register(Comment)
