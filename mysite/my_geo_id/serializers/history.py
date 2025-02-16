from rest_framework import serializers

from ..models import (
    GeoObject,
    GeoObjectMap,
)


class GeoObjectHistorySerializer(serializers.ModelSerializer):
    """
    Получения исторических записей Геообъекта(GeoObject)
    """

    class Meta:
        model = GeoObject.history.model
        fields = "is_active", "object_code", "object_name",


class GeoObjectMapHistorySerializer(serializers.ModelSerializer):
    """
    Получения исторических записей связей геообъекта(GeoObjectMap)
    """
    # main_name = serializers.CharField(source='main.object_name', read_only=True)
    # sub_name = serializers.CharField(source='sub.object_name', read_only=True)
    # map_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GeoObjectMap.history.model
        fields = "is_active", "main", "sub",
        # fields = ['main', 'main_name', 'sub', 'sub_name', 'map_type']
