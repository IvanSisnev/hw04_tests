"""
Файл с тестами форм моделей.
"""

from typing import Dict, Any

from django import forms
from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests
from ..models import Post


class FormsTests(PostsTests):
    """
    Класс для проверки правильности форм на страницах.
    """

    def setUp(self):
        """
        Создает авторизованного пользователя.
        """
        self.authorized_client = Client()
        self.authorized_client.force_login(FormsTests.user)

    def test_form_fields_type(self):
        """
        Проверить правильность передаваемых форм.
        """

        form_fields: Dict[str, Any] = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        # проверка правильности формы страницы редактирования записи
        reverse_name = 'posts:post_edit'
        param = {'post_id': FormsTests.post.id}
        response = self.authorized_client.get(reverse(reverse_name,
                                                      kwargs=param))
        for field, field_type in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, field_type)

        # проверка правильности формы страницы создания записи
        reverse_name = 'posts:post_create'
        response = self.authorized_client.get(reverse(reverse_name))

        for field, field_type in form_fields.items():
            with self.subTest(field=field):
                form_field = response.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, field_type)

    def test_post_create(self):
        """
        Проверить создание новой записи.
        """
        post_count = Post.objects.count()

        form_data: Dict[str, Any] = {
            'text': 'Текст нового поста',
            'author': FormsTests.user,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data, follow=True)

        # проверка добавления новой записи в БД
        self.assertEqual(Post.objects.count(), post_count + 1)
        # проверка созданной записи
        self.assertTrue(Post.objects.filter(text=form_data['text']).exists())

    def test_post_edit(self):
        """
        Проверить редактирование существующей записи.
        """
        new_text = 'Отредактированный текст нового поста'
        form_data: Dict[str, str] = {
            'text': new_text,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': FormsTests.post.id}),
            data=form_data, follow=True)

        # проверка успешного изменения записи
        edited_post = Post.objects.get(id=FormsTests.post.id)
        self.assertEqual(edited_post.text, new_text)
