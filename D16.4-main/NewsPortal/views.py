from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, PostCategory, SubscribeCategory, Author
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User


class PostList(LoginRequiredMixin, ListView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post  # не моуг понять почему при вставке заместо модел queryset = Post.objects.order_by('-publication_date')
    # не определяется обьект, по коду из технической документации с помощью этой строчки можно фильтровать дату публикации
    ordering = 'header_post'
    # Используем другой шаблон — product.html
    template_name = 'posts.html'
    # фильтрует буликации по дате создания
    # queryset = Post.objects.order_by('-time_in')
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'posts'

    paginate_by = 4  # вот так мы можем указать количество записей на странице

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        # Чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = list(PostCategory.objects.filter(
            post=self.kwargs['pk']).values('category', 'category__name'))
        check_subscribe = list(SubscribeCategory.objects.filter(subscribers=self.request.user.id).values('category'))
        context['subscribe'] = [n['category'] for n in check_subscribe]
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post')
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author = self.request.user.author
        path = self.request.META['PATH_INFO']
        if path == '/article/create/':
            post.type_post = 'article'

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    # permission_required = ('newstrueapp.add_post')
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'


# Представление удаляющее товар.
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ProfilAuthor(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'profil_user.html'

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context



@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    Author.objects.create(author=user)
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    return redirect('/')


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    return redirect('/')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    return redirect('/')

