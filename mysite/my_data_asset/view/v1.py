from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from ..models import Asset, AssetStat
from ..serializers import AssetSerializer, AssetStatSerializer


@extend_schema(
    tags=["Data asset"],
    summary="DataAssetAPIViewSet",
    description=(
            """
            Обработка источников данных.
            """
    ),
)
class DataAssetAPIViewSet(ModelViewSet):
    """
    Получить список всех DataAssetAPIViewSet.
    1) Запросы 'POST','PUT','PATCH','DELETE' - требуем авторизацию!!!
    """

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):

        if self.request.method in ['GET', ]:
            # Разрешаем доступ для неавторизованных пользователей
            self.permission_classes = [permissions.AllowAny]
        else:
            # Если метод запроса - это создание, обновление или удаление, требуем авторизацию
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    @extend_schema(
        summary='Получить список всех "Источник данных".',
        description='Возвращает список всех доступных "Источник данных".',
        tags=["Data asset"],

    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Создать новый "Источник данных"',
        description='Создает новый объект "Источник данных".',
        tags=["Data asset"],

    )
    def create(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Получить "Источник данных" по ID',
        description='Возвращает объект "Источник данных" по указанному ID.',
        tags=["Data asset"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Обновить существующий "Источник данных"',
        description='Обновляет объект "Источник данных" по указанному ID.',
        tags=["Data asset"]
    )
    def update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Частичное обновление "Источник данных"',
        description='Частично обновляет объект "Источник данных" по указанному ID.',
        tags=["Data asset"]
    )
    def partial_update(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary='Удалить "Источник данных"',
        description='Удаляет объект "Источник данных" по указанному ID.',
        tags=["Data asset"]
    )
    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)  # Проверка разрешений
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    tags=["Data asset"],
    summary="DataAssetAPIViewSet",
    description=(
            """
            Обработка источников данных.
            """
    ),
)
class AssetStatAPIViewSet(ModelViewSet):
    queryset = AssetStat.objects.all()
    serializer_class = AssetStatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    @extend_schema(
        summary="Список источников данных",
        description="Извлечение списка источников данных",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание новый ресурс данных",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Извлечение определенного источника данных",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление определенного источника данных",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Удаление определенного источника данных",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление определенного источника данных",
        description="Частичное обновление определенного источника данных по его ID. Укажите только те поля, которые хотите обновить.",
        request=AssetStatSerializer,
        responses={200: AssetStatSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
