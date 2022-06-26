from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template.loader import render_to_string

from .forms import *
from .models import *
from .utils import *

import json
from django.views import View
from django.contrib.contenttypes.models import ContentType
 

def index(request):
    return render(request, "index.html", {})

def home(request):
    return render(request, "home.html", {})

def about_us(request):
    return render(request, "index.html", {})

def contact(request):
    return render(request, "contact.html", {})

def login(request):
    return render(request, "registration/login.html")

def logout(request):
    return render(request, "registration/logged_out.html")

def quotes(request):
    return render(request, "quotes.html")

def add_page_err(request):
    return render(request, "add_page_err.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"

def password_reset(request):
    return render(request, "password_reset_form.html", {})

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'addpage.html'
    success_url = reverse_lazy('articles')
    login_url = reverse_lazy('add_page_err')
    raise_exception = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Adding an article")
        return dict(list(context.items()) + list(c_def.items()))



class ShowPost(DataMixin, DetailView):
    model = Article
    template_name = 'post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Article, slug=(self.request.get_full_path().split('/'))[2] )
        count_likes = len(post.likes.all())
        context['count_likes']=count_likes
        print("--------------")
        print((self.request.get_full_path().split('/'))[2])
        print("--------------")
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))
      

class ArticleCategory(DataMixin, ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Article.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
        cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class SaybookHome(DataMixin, ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

class SearchResultsView(ListView):
    model = Article
    template_name = 'search_results.html'
 
    def get_queryset(self): # новый
        query = self.request.GET.get('q')
        object_list = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list


 
def like_post(request):
    post = get_object_or_404(Article, id=request.POST.get('id'))    
    is_liked = False
    count_likes = len(post.likes.all())
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        count_likes-=1
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
        count_likes+=1
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'count_likes': count_likes
    }
    if request.is_ajax():
        html = render_to_string('like_section.html', context, request=request)
        return JsonResponse({'form': html})

