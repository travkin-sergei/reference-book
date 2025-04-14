from rest_framework import serializers

from ..models import (
    Object,
    ObjectMap,
)


class ObjectHistorySerializer(serializers.ModelSerializer):
    """
    Получения исторических записей Геообъекта(Object)
    """

    class Meta:
        model = Object.history.model
        fields = "is_active", "object_code", "object_name",


class ObjectMapHistorySerializer(serializers.ModelSerializer):
    """
    Получения исторических записей связей геообъекта(ObjectMap)
    """
    # main_name = serializers.CharField(source='main.object_name', read_only=True)
    # sub_name = serializers.CharField(source='sub.object_name', read_only=True)
    # map_type = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ObjectMap.history.model
        fields = "is_active", "main", "sub",
        # fields = ['main', 'main_name', 'sub', 'sub_name', 'map_type']
