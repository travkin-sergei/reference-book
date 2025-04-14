from rest_framework import serializers
from ..models import (
    Synonym,
    Object,
    ObjectMap, ObjectMapSub,
    ObjectCodeType,
    ObjectCode,
)


class SynonymSerializer(serializers.ModelSerializer):
    """Сериализация для отображения в DataAssetSerializer."""

    class Meta:
        model = Synonym
        fields = 'name', 'language',


class ObjectMapSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectMapSub
        fields = [
            'id',  # Поле ID
            'object_code',  # Внешний ключ на ObjectMap
            'object',  # Внешний ключ на Object
            'code_type',  # Внешний ключ на ObjectMapType
            'date_start',  # Дата начала действия
            'date_stop',  # Дата прекращения действия
        ]


class ObjectMapSerializer(serializers.ModelSerializer):
    related_objects = ObjectMapSubSerializer(many=True, read_only=True)

    class Meta:
        model = ObjectMap
        fields = 'id', 'is_active', 'main', 'related_objects',


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = '__all__'
        # fields = 'object_code', 'object_name', 'date_start', 'date_stop',
