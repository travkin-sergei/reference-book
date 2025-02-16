from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from ..serializers import *

tags = ["GEO-ID", ]


@extend_schema(tags=["geo_object"], summary="GeoNamesViewSet", description=("""Названия."""), )
class GeoNamesViewSet(ModelViewSet):
    """
    Получить список всех DataAssetAPIViewSet.
    1) Запросы 'POST','PUT','PATCH','DELETE' - требуем авторизацию!!!
    """

    queryset = GeoNames.objects.all()
    serializer_class = GeoNamesSerializer
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


@extend_schema(tags=["geo_object_sub"], summary="GeoObjectMapSubViewSet", description=("""Описание."""), )
class GeoObjectMapSubViewSet(ModelViewSet):
    """
    Получить список всех GeoObjectMapSub.
    1) Запросы 'POST','PUT','PATCH','DELETE' - требуем авторизацию!!!
    """

    queryset = GeoObjectMapSub.objects.all()
    serializer_class = GeoObjectMapSubSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # Если метод запроса - это создание, обновление или удаление, требуем авторизацию
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]  # Разрешаем доступ для неавторизованных пользователей
        return super().get_permissions()

    @extend_schema(
        summary='Список GeoObjectMapSub',
        description='Получить список всех GeoObjectMapSub.',
        tags=["geo_object_sub"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Создать GeoObjectMapSub',
        description='Создать новый объект GeoObjectMapSub.',
        tags=["geo_object_sub"],
    )
    def create(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Получить GeoObjectMapSub',
        description='Получить объект GeoObjectMapSub по ID.',
        tags=["geo_object_sub"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Обновить GeoObjectMapSub',
        description='Обновить объект GeoObjectMapSub по ID.',
        tags=["geo_object_sub"],
    )
    def update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Частичное обновление GeoObjectMapSub',
        description='Частично обновить объект GeoObjectMapSub по ID.',
        tags=["geo_object_sub"],
    )
    def partial_update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Удалить GeoObjectMapSub',
        description='Удалить объект GeoObjectMapSub по ID.',
        tags=["geo_object_sub"],
    )
    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().destroy(request, *args, **kwargs)


class GeoObjectSearchView(ModelViewSet):
    queryset = GeoObject.objects.all()
    serializer_class = GeoObjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
