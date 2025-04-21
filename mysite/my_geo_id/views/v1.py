from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import Synonym
from ..serializers import *

tags = ["GEO-ID", ]


@extend_schema(tags=["object"], summary="SynonymViewSet", description=("""Названия."""), )
class SynonymViewSet(ModelViewSet):
    """
    Получить список всех DataAssetAPIViewSet.
    1) Запросы 'POST','PUT','PATCH','DELETE' - требуем авторизацию!!!
    """

    queryset = Synonym.objects.all()
    serializer_class = SynonymSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # Если метод запроса - это создание, обновление или удаление, требуем авторизацию
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]  # Разрешаем доступ для неавторизованных пользователей
        return super().get_permissions()

    @extend_schema(
        summary='Получить список всех "Названий geo-id".',
        description='Возвращает список всех доступных "Названий geo-id".',
        tags=tags,

    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Создать новое "Название geo-id"',
        description='Создает новый объект "Названий geo-id".',
        tags=tags,

    )
    def create(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Получить "Название geo-id" по ID',
        description='Возвращает объект "Название geo-id" по указанному ID.',
        tags=tags
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Обновить существующее "Название geo-id"',
        description='Обновляет объект "Название geo-id" по указанному ID.',
        tags=tags
    )
    def update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Частичное обновление "Названия geo-id"',
        description='Частично обновляет объект "Название geo-id" по указанному ID.',
        tags=tags
    )
    def partial_update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Удалить "Название geo-id"',
        description='Удаляет объект "Название geo-id" по указанному ID.',
        tags=tags
    )
    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=["object_sub"], summary="ObjectMapSubViewSet", description=("""Описание."""), )
class ObjectMapSubViewSet(ModelViewSet):
    """
    Получить список всех ObjectMapSub.
    1) Запросы 'POST','PUT','PATCH','DELETE' - требуем авторизацию!!!
    """

    queryset = ObjectMapSub.objects.all()
    serializer_class = ObjectMapSubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # Если метод запроса - это создание, обновление или удаление, требуем авторизацию
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]  # Разрешаем доступ для неавторизованных пользователей
        return super().get_permissions()

    @extend_schema(
        summary='Список ObjectMapSub',
        description='Получить список всех ObjectMapSub.',
        tags=tags
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Создать ObjectMapSub',
        description='Создать новый объект ObjectMapSub.',
        tags=tags
    )
    def create(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Получить ObjectMapSub',
        description='Получить объект ObjectMapSub по ID.',
        tags=tags
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Обновить ObjectMapSub',
        description='Обновить объект ObjectMapSub по ID.',
        tags=tags
    )
    def update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Частичное обновление ObjectMapSub',
        description='Частично обновить объект ObjectMapSub по ID.',
        tags=tags
    )
    def partial_update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Удалить ObjectMapSub',
        description='Удалить объект ObjectMapSub по ID.',
        tags=tags
    )
    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().destroy(request, *args, **kwargs)


class ObjectSearchView(ModelViewSet):
    queryset = Object.objects.all()
    serializer_class = ObjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
