import django_filters
from .models import (
    GeoObject,
    GeoObjectCode,
    GeoObjectMap,
)


class GeoObjectFilter(django_filters.FilterSet):
    """Фильтрация GeoObject."""

    object_code = django_filters.CharFilter(
        field_name='object_code', lookup_expr='icontains', label='geo-id'
    )
    object_name = django_filters.CharFilter(
        field_name='object_name', lookup_expr='icontains', label='техническое название'
    )

    class Meta:
        model = GeoObject
        fields = 'object_code', 'object_name',


class GeoObjectCodeFilter(django_filters.FilterSet):
    """Фильтрация GeoObjectCode."""

    main = django_filters.CharFilter(field_name='main__object_name', lookup_expr='icontains', label='Основной объект')
    code_type = django_filters.CharFilter(field_name='code_type__code_type', lookup_expr='icontains', label='Тип кода')

    class Meta:
        model = GeoObjectCode
        fields = 'main', 'code_type',


class GeoObjectMapFilter(django_filters.FilterSet):
    """Фильтрация GeoObjectMap."""

    main = django_filters.CharFilter(field_name='main__object_name', lookup_expr='icontains', label='Основной объект')

    class Meta:
        model = GeoObjectMap
        fields = 'main',
