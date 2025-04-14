import django_filters
from .models import (
    Object,
    ObjectCode,
    ObjectMap,
)


class ObjectFilter(django_filters.FilterSet):
    """Фильтрация Object."""

    object_code = django_filters.CharFilter(
        field_name='object_code', lookup_expr='icontains', label='geo-id'
    )
    object_name = django_filters.CharFilter(
        field_name='object_name', lookup_expr='icontains', label='техническое название'
    )

    class Meta:
        model = Object
        fields = 'object_code', 'object_name',


class ObjectCodeFilter(django_filters.FilterSet):
    """Фильтрация ObjectCode."""

    main = django_filters.CharFilter(field_name='main__object_name', lookup_expr='icontains', label='Основной объект')
    code_type = django_filters.CharFilter(field_name='code_type__code_type', lookup_expr='icontains', label='Тип кода')

    class Meta:
        model = ObjectCode
        fields = 'main', 'code_type',


class ObjectMapFilter(django_filters.FilterSet):
    """Фильтрация ObjectMap."""

    main = django_filters.CharFilter(field_name='main__object_name', lookup_expr='icontains', label='Основной объект')

    class Meta:
        model = ObjectMap
        fields = 'main',
