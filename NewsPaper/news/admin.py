from .models import Author, Category, Post, PostCategory, Comment
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

# напишем уже знакомую нам функцию обнуления
def nullfy_rating(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)
    nullfy_rating.short_description = 'Обнулить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
# list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'categoryType', 'author', 'rating')  # генерируем список имён всех полей для более красивого отображения
    list_filter = ('categoryType', 'author', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('title', 'categoryType', 'author')  # тут всё очень похоже на фильтры из запросов в базу
    actions = [nullfy_rating]  # добавляем действия в список

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)