"""
Файл с тестами view-функций проекта.
"""

from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests


class ViewsTests(PostsTests):
    """
    Класс для проверки правильности шаблонов во view-функциях.
    """

    def setUp(self):
        """
        Создает авторизованного пользователей.
        """
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_views_templates(self):
        """
        Проверяет правильность шаблонов во view-функциях.
        """

        # проверка соответствия шаблонов и reverse(name)
        for reverse_name, url_data in self.pages_dict.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(
                    reverse(reverse_name, kwargs=url_data['param']))
                self.assertTemplateUsed(response, url_data['template'])

    def test_views_context(self):
        """
        Проверяет правильность переданного контекста.
        """
        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'context' in page_data:
                    response = self.authorized_client.get(
                        reverse(page_name, kwargs=page_data['param'])
                    )
                    if 'test_method' in page_data['context']:
                        self.assertEqual(page_data['context'][
                            'test_method'](
                            response.context[
                                page_data['context']['variable']]),
                            page_data['context']['data'])
                    else:
                        self.assertEqual(response.context[
                                             page_data['context']['variable']
                                         ],page_data['context']['data'])

    def test_post(self):
        """
        Проверяет, что созданная запись отображается на нужных
        страницах.
        """

        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'paginator' in page_data:
                    response = self.authorized_client.get(reverse(
                        page_name, kwargs=page_data['param']))
                    self.assertContains(response, self.post)
