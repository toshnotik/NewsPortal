from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author
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

    class Meta:
        model = Post
        fields = []
