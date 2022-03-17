from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Post, Author, Category, PostCategory
from django.forms import DateInput


class PostFilter(FilterSet):
    datetime = DateFilter(
        field_name='dateCreation',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Позже:'
    )

    title = CharFilter(
        field_name='title',
        label='Заголовок содержит:',
        lookup_expr='icontains',
    )

    author = ModelChoiceFilter(
        field_name='author',
        label='Автор:',
        lookup_expr='exact',
        queryset=Author.objects.all()
    )

    PostCategory = ModelChoiceFilter(
        field_name='PostCategory',
        label='Категория:',
        lookup_expr='exact',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = []
