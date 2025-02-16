from rest_framework import serializers
from ..models import (
    GeoNames,
    GeoObject,
    GeoObjectMap, GeoObjectMapSub,
    GeoObjectCodeType,
    GeoObjectCode,
)


class GeoNamesSerializer(serializers.ModelSerializer):
    """Сериализация для отображения в DataAssetSerializer."""

    class Meta:
        model = GeoNames
        fields = 'name', 'language',


class GeoObjectMapSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoObjectMapSub
        fields = [
            'id',  # Поле ID
            'geo_object_code',  # Внешний ключ на GeoObjectMap
            'geo_object',  # Внешний ключ на GeoObject
            'code_type',  # Внешний ключ на GeoObjectMapType
            'date_start',  # Дата начала действия
            'date_stop',  # Дата прекращения действия
        ]


class GeoObjectMapSerializer(serializers.ModelSerializer):
    related_objects = GeoObjectMapSubSerializer(many=True, read_only=True)

    class Meta:
        model = GeoObjectMap
        fields = 'id', 'is_active', 'main', 'related_objects',


class GeoObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoObject
        fields = '__all__'
        # fields = 'object_code', 'object_name', 'date_start', 'date_stop',
