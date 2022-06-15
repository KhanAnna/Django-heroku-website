from django.urls import path, re_path

from . import views
from .models import LikeDislike, Article
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.SaybookHome.as_view(), name='home'),
    path('articles/', views.articles, name='articles'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('about_us/', views.about_us, name='about_us'),
    path('quotes/', views.quotes, name='quotes'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.ArticleCategory.as_view(), name='category'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
  
    path('like/', views.like_post, name="like_post"),

]