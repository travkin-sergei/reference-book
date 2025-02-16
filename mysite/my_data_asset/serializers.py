from rest_framework import serializers
from .models import (
    DataAsset,
    DataAssetType,
    DataAssetStatus,
)


class DataAssetTypeSerializer(serializers.ModelSerializer):
    """Сериализация для отображения в DataAssetSerializer."""

    class Meta:
        model = DataAssetType
        fields = 'name',


class DataAssetStatusSerializer(serializers.ModelSerializer):
    """Сериализация для отображения в DataAssetSerializer."""

    class Meta:
        model = DataAssetStatus
        fields = 'name',


class DataAssetSerializer(serializers.ModelSerializer):
    """Сериализация списка источников данных."""

    type = serializers.CharField(source='type.name', read_only=True)
    status = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = DataAsset
        fields = [
            'hash_address', 'last_update',
            'uir', 'url',
            'name', 'comment', 'version',
            'host', 'port',
            'type', 'status',
        ]

    def to_representation(self, instance):
        """
        Переопределяем метод to_representation для ограничения полей.
        1. Получаем текущего пользователя из контекста
        2. Проверяем, принадлежит ли пользователь к группе 'devops' или является супер администратором
        3. Убираем поля 'host' и 'port', если пользователь не в группе 'devops' и не супер администратор
        """

        representation = super().to_representation(instance)
        # 1.
        request = self.context.get('request')
        user = request.user if request else None
        # 2.
        if user and not (user.groups.filter(name='devops').exists() or user.is_superuser):
            # 3.
            representation.pop('host', None)
            representation.pop('port', None)

        return representation
