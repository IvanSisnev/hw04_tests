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
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание'
        )

        # создание нужного количества тестовых записей
        post_list = []
        for i in range(14):
            post_list.append(Post(text=f'Тестовая запись - текст поста {i}',
                                  author=cls.user, group=cls.group))
        Post.objects.bulk_create(post_list)
        cls.post = Post.objects.first()

        # словарь, в котором ключ это name_space:name, а значение - словарь с
        # url-aдресом, параметром адреса, шаблоном страницы, уровнем
        # доступа к странице, наличием паджинатора, параметрами для проверки
        # контекста
        cls.pages_dict = {
            'posts:index': {
                'url': '/',
                'param': None,
                'template': 'posts/index.html',
                'access': 'unlimited',
                'paginator': True,
                'context': {
                    'variable': 'posts',
                    'test_method': list,
                    'data': list(Post.objects.all())
                }
            },
            'posts:post_create': {
                'url': '/create/',
                'param': None,
                'template': 'posts/create_post.html',
                'form': True,
                'access': 'limited',
            },
            'posts:profile': {
                'url': f'/profile/{cls.user.username}/',
                'param': {'username': cls.user.username},
                'template': 'posts/profile.html',
                'access': 'unlimited',
                'paginator': True,
                'context': {
                    'variable': 'posts',
                    'test_method': list,
                    'data': list(cls.user.posts.all())
                }
            },
            'posts:group_list': {
                'url': f'/group/{cls.group.slug}/',
                'param': {'slug': cls.group.slug},
                'template': 'posts/group_list.html',
                'access': 'unlimited',
                'paginator': True,
                'context': {
                    'variable': 'posts',
                    'test_method': list,
                    'data': list(cls.group.posts.all()),
                }
            },
            'posts:post_detail': {
                'url': f'/posts/{cls.post.id}/',
                'param': {'post_id': cls.post.id},
                'template': 'posts/post_detail.html',
                'access': 'unlimited',
                'context': {
                    'variable': 'post',
                    'data': Post.objects.get(pk=cls.post.id),
                }
            },
            'posts:post_edit': {
                'url': f'/posts/{cls.post.id}/edit/',
                'param': {'post_id': cls.post.id},
                'template': 'posts/create_post.html',
                'form': True,
                'access': 'limited',
                'context': {
                    'variable': 'post',
                    'data': Post.objects.get(pk=cls.post.id),
                }
            },
        }

    @classmethod
    def tearDownClass(cls):
        """
        Приборка после тестов.
        """
        super().tearDownClass()
