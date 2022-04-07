
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'categoryType', 'postCategory']
        labels = {
            'title': 'Заголовок:',
            'text': 'Текст статьи:',
            'author': 'Автор:',
            'categoryType': 'Тип статьи:',
            'postCategory': 'Рубрика:',
        }


