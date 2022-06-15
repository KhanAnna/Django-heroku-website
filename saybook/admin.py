from django.contrib import admin

from .models import *
# from django.contrib.admin.views.main import ChangeList
from .models import Article
# from .forms import ArticleChangeListForm

# class ArticleChangeList(ChangeList):

#     def __init__(self, request, model, list_display,
#         list_display_links, list_filter, date_hierarchy,
#         search_fields, list_select_related, list_per_page,
#         list_max_show_all, list_editable, model_admin):

#         super(ArticleChangeList, self).__init__(request, model,
#             list_display, list_display_links, list_filter,
#             date_hierarchy, search_fields, list_select_related,
#             list_per_page, list_max_show_all, list_editable, 
#             model_admin)

#         # these need to be defined here, and not in ArticleAdmin
#         self.list_display = ['action_checkbox', 'name', 'genre']
#         self.list_display_links = ['name']
#         self.list_editable = ['genre']


# class ArticleAdmin(admin.ModelAdmin):

#     def get_changelist(self, request, **kwargs):
#         return ArticleChangeList

#     def get_changelist_form(self, request, **kwargs):
#         return ArticleChangeListForm




class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
