from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Post, Category, Author, User, Comment
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.core.cache import cache


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        return context


class CategoriesList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'postcategories'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sub_user = Category.objects.values('subscribers')
        context['is_not_sub'] = not sub_user.filter(subscribers=self.request.user).exists()
        context['is_sub'] = sub_user.filter(subscribers=self.request.user).exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
        }


class PostEdit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostAdd(PermissionRequiredMixin, CreateView):
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post',)


@login_required
def add_subscriber(request, pk):
    Category.objects.get(pk=pk)
    Category.objects.get(pk=pk).subscribers.add(request.user)
    user = request.user
    id_u = user.id
    category = Category.objects.get(id=pk)
    email = category.subscribers.get(id=id_u).email
    send_mail(
        subject=f'News Portal: подписка на обновления категории {category}',
        message=f'«{request.user}», вы подписались на обновление категории: «{category}».',
        from_email='skillfactor@yandex.ru',
        recipient_list=[f'{email}', ],
        )
    return redirect('/news/category/')


@login_required
def del_subscriber(request, pk):
    Category.objects.get(pk=pk)
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/category/')
