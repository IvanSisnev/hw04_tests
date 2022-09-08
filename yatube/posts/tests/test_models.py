"""
Файл с тестами моделей проекта.
"""

from typing import Dict

from .tests_setup import PostsTests


class PostModelTest(PostsTests):
    """
    Класс тестирования модели Post.
    """

    def test_object_name(self):
        """
        Результат метода __str__ совпадает с ожидаемым.
        """
        # для модели Post
        post = PostModelTest.post
        result = post.__str__()
        norm = f'{post.text[:15]}'
        self.assertEqual(result, norm)

        # для модели Group
        group = PostModelTest.group
        result = group.__str__()
        norm = f'{group.title}'
        self.assertEqual(result, norm)

    def test_verbose(self):
        """
        Наименования полей совпадают с ожидаемыми.
        """
        # для модели Post
        post = PostModelTest.post
        post_field_verbose: Dict[str, str] = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор поста',
            'group': 'Сообщество',
        }
        for field, expected_value in post_field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(post._meta.get_field(field).verbose_name,
                                 expected_value)

        # для модели Group
        group = PostModelTest.group
        group_field_verbose: Dict[str, str] = {
            'title': 'Название группы',
            'slug': 'Слаг группы',
            'description': 'Описание группы',
        }
        for field, expected_value in group_field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(group._meta.get_field(field).verbose_name,
                                 expected_value)

    def test_help_text(self):
        """
        Вспомогательные тексты совпадают с ожидаемыми.
        """
        # для модели Post
        post = PostModelTest.post
        post_help_text: Dict[str, str] = {
            'text': 'Поле для текста поста',
            'author': 'Выберите автора',
            'group': 'Необязательно: выберите сообщество',
        }
        for field, expected_value in post_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(post._meta.get_field(field).help_text,
                                 expected_value)

        # для модели Group
        group = PostModelTest.group
        group_help_text: Dict[str, str] = {
            'title': 'Поле для названия сообщества',
            'slug': 'Короткий универсальный идентификатор сообщества',
            'description': 'Поле для короткого описания сообщества',
        }
        for field, expected_value in group_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(group._meta.get_field(field).help_text,
                                 expected_value)
