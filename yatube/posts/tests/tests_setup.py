"""
Файл с установками и фикстурами для тестов.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Post, Group

User = get_user_model()


class PostsTests(TestCase):
    """
    Родительский класс с созданием фикстур для классов тестов.
    """

    @classmethod
    def setUpClass(cls):
        """
        Создает фикстуры тестов модели.
        """

        super().setUpClass()
        # создание тестового пользователя
        cls.user = User.objects.create_user(username='NoName')

        # создание тестовой группы
        cls.group = Group.objects.create(
            title='Тестовое название',
            slug='test_slug',
            description='Тестовое описание'
        )
        # создание достаточного количества тестовых записей
        for i in range(14):
            cls.post = Post.objects.create(
                text=f'Тестовая запись - текст поста {i}',
                author=cls.user,
                group=cls.group
            )

    @classmethod
    def tearDownClass(cls):
        """
        Приборка после тестов.
        """
        super().tearDownClass()
