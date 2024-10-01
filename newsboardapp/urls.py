from django.urls import path
from django.contrib.auth.decorators import login_required
# Импортируем созданное нами представление
from .views import (PostList,
                    PostDetail,
                    craate_post,
                    ArticleList,
                    ArticleDetail,
                    PostUpdate,
                    PostCreate,
                    PostDelete,
                    ArticleCreate,
                    ArticleUpdate,
                    ArticleDelete,

                    CatList,
                    CatDetail,
                    CatUpdate,
                    CatCreate,
                    CatDelete,
                    subscribe_cat,
                    )


urlpatterns = [
   path('articles/', login_required(ArticleList.as_view()),name='articles'),
   path('articles/<int:pk>', login_required(ArticleDetail.as_view()), name='article'),
   path('articles/create/', login_required(ArticleCreate.as_view()), name='article_create'),
   path('articles/<int:pk>/update/', login_required(ArticleUpdate.as_view()), name='article_update'),
   path('articles/<int:pk>/delete/', login_required(ArticleDelete.as_view()), name='article_delete'),

   path('news/', login_required(PostList.as_view()),name='news'),
   path('news/<int:pk>', login_required(PostDetail.as_view()),name='post'),
   #path('news/create/', craate_post,name='post_create'),
   path('news/create/', login_required(PostCreate.as_view()),name='post_create'),
   path('news/<int:pk>/update/', login_required(PostUpdate.as_view()), name='post_update'),
   path('news/<int:pk>/delete/', login_required(PostDelete.as_view()), name='post_delete'),


path('cats/', login_required(CatList.as_view()),name='cats'),
   path('cats/<int:pk>', login_required(CatDetail.as_view()),name='cat'),
   path('cats/create/', login_required(CatCreate.as_view()),name='cat_create'),
   path('cats/<int:pk>/update/', login_required(CatUpdate.as_view()), name='cat_update'),
   path('cats/<int:pk>/delete/', login_required(CatDelete.as_view()), name='cat_delete'),
   path('cats/subscribe/', subscribe_cat, name='subscribe_cat'),
]