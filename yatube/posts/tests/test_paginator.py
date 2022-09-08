"""
Файл с тестами паджинации страниц.
"""

from typing import Dict, Any

from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests


class PaginatorTests(PostsTests):
    """
    Класс для проверки правильности паджинации.
    """

    def setUp(self):
        """
        Создает авторизованного пользователя.
        """
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorTests.user)

    def test_paginator(self):
        """
        Проверить правильность работы поджинатора на страницах.
        """
        reverse_names_kwargs: Dict[str, Any] = {
            'posts:index': None,
            'posts:profile': {'username': PaginatorTests.user.username},
            'posts:group_list': {'slug': PaginatorTests.group.slug},
        }

        for reverse_name, param in reverse_names_kwargs.items():
            # проверка первой страницы
            response = self.authorized_client.get(reverse(reverse_name,
                                                          kwargs=param))
            self.assertEqual(len(response.context['page_obj']), 10)
            # проверка второй страницы
            response = self.authorized_client.get(
                reverse(reverse_name, kwargs=param) + '?page=2')
            self.assertEqual(len(response.context['page_obj']), 4)
