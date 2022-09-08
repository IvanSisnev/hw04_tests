"""
Файл с тестами URLs проекта.
"""

from http import HTTPStatus
from typing import Dict, List

from django.test import Client

from .tests_setup import PostsTests


class UrlTests(PostsTests):
    """
    Класс для проверки доступности страниц и шаблонов.
    """

    def setUp(self):
        """
        Создает неавторизованного и авторизованного пользователей.
        """
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(UrlTests.user)

    def test_urls_access(self):
        """
        Проверяет доступность страниц.
        """
        # список страниц с неограниченным доступом
        urls_unlimited_access: List[str] = [
            '/',
            f'/group/{UrlTests.group.slug}/',
            f'/profile/{UrlTests.user.username}/',
            f'/posts/{UrlTests.post.id}/',
        ]
        # проверка доступа для неавторизованного пользователя
        for url in urls_unlimited_access:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        # список страниц с ограниченным доступом
        urls_limited_access: List[str] = [
            f'/posts/{UrlTests.post.id}/edit/',
            '/create/',
        ]
        for url in urls_limited_access:
            with self.subTest(url=url):
                # проверка переадресации неавторизованного пользователя
                self.get = self.guest_client.get(url)
                response = self.get
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

                # проверка доступа для авторизованного пользователя
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

        # проверка доступа к несуществующей странице
        response = self.guest_client.get('/nonexistent_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_templates(self):
        """
        Проверяет правильность шаблонов страниц.
        """
        # словарь с адресами страниц и их шаблонами
        urls_templates: Dict[str, str] = {
            '/': 'posts/index.html',
            f'/group/{UrlTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{UrlTests.user.username}/': 'posts/profile.html',
            f'/posts/{UrlTests.post.id}/': 'posts/post_detail.html',
            f'/posts/{UrlTests.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }

        for url, template in urls_templates.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template_name=template)
