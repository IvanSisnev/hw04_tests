"""
Файл с тестами view-функций проекта.
"""

from typing import Dict, Tuple, Any

from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests
from ..models import Post


class ViewsTests(PostsTests):
    """
    Класс для проверки правильности шаблонов во view-функциях.
    """

    def setUp(self):
        """
        Создает неавторизованного и авторизованного пользователей.
        """
        self.authorized_client = Client()
        self.authorized_client.force_login(ViewsTests.user)

    def test_views_templates(self):
        """
        Проверяет правильность шаблонов во view-функциях.
        """

        # словарь, где ключ это reverse(name), а значение - параметр url и
        # шаблон
        reverse_names_params_templates: Dict[str, Tuple[Any, str]] = {
            'posts:index': (
                None,
                'posts/index.html',
            ),
            'posts:post_create': (
                None,
                'posts/create_post.html',
            ),
            'posts:profile': (
                {'username': ViewsTests.user.username},
                'posts/profile.html',
            ),
            'posts:group_list': (
                {'slug': ViewsTests.group.slug},
                'posts/group_list.html',
            ),
            'posts:post_detail': (
                {'post_id': ViewsTests.post.id},
                'posts/post_detail.html',
            ),
            'posts:post_edit': (
                {'post_id': ViewsTests.post.id},
                'posts/create_post.html',
            ),
        }
        # проверка соответствия шаблонов и reverse(name)
        # data[0] это параметр url, data[1] - шаблон
        for reverse_name, data in reverse_names_params_templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(
                    reverse(reverse_name, kwargs=data[0]))
                self.assertTemplateUsed(response, data[1])

    def test_views_context_and_forms(self):
        """
        Проверяет правильность переданного контекста.
        """
        # проверка контекста главной страницы
        reverse_name = 'posts:index'
        data = Post.objects.all()
        response = self.authorized_client.get(reverse(reverse_name))
        self.assertEqual(list(response.context['posts']), list(data))

        # проверка контекста страницы записей сообщества
        reverse_name = 'posts:group_list'
        param = {'slug': ViewsTests.group.slug}
        data = ViewsTests.group.posts.all()
        response = self.authorized_client.get(reverse(reverse_name,
                                                      kwargs=param))
        self.assertEqual(list(response.context['posts']), list(data))

        # проверка контекста страницы пользователя
        reverse_name = 'posts:profile'
        param = {'username': ViewsTests.user.username}
        data = ViewsTests.user.posts.all()
        response = self.authorized_client.get(reverse(reverse_name,
                                                      kwargs=param))
        self.assertEqual(list(response.context['posts']), list(data))

        # проверка контекста страницы записи
        reverse_name = 'posts:post_detail'
        param = {'post_id': ViewsTests.post.id}
        datum = Post.objects.get(pk=ViewsTests.post.id)
        response = self.authorized_client.get(reverse(reverse_name,
                                                      kwargs=param))
        self.assertEqual(response.context['post'], datum)

        # проверка контекста страницы редактирования записи
        reverse_name = 'posts:post_edit'
        param = {'post_id': ViewsTests.post.id}

        datum = Post.objects.get(pk=ViewsTests.post.id)
        response = self.authorized_client.get(reverse(reverse_name,
                                                      kwargs=param))
        self.assertEqual(response.context['post'], datum)

    def test_post(self):
        """
        Проверяет, что созданная запись отображается на нужных страницах.
        """
        # словарь страниц для проверки
        reverse_names_kwargs: Dict[str, Any] = {
            'posts:index': None,
            'posts:profile': {'username': ViewsTests.user.username},
            'posts:group_list': {'slug': ViewsTests.group.slug},
        }

        for reverse_name, datum in reverse_names_kwargs.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse(reverse_name,
                                                              kwargs=datum))
                self.assertTrue(ViewsTests.post in response.context['posts'])
