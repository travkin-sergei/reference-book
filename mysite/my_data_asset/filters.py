import django_filters
from django_filters import CharFilter
from .models import (
    DataAsset,
    DataModel,
    DataAssetGroup,
)


class DataAssetFilter(django_filters.FilterSet):
    """Фильтрация источников данных."""

    uir = CharFilter(field_name='uir', lookup_expr='icontains', )
    name = CharFilter(field_name='name', lookup_expr='icontains', )
    url = CharFilter(field_name='url', lookup_expr='icontains', )
    comment = CharFilter(field_name='comment', lookup_expr='icontains', )
    host = CharFilter(field_name='host', lookup_expr='icontains', )
    port = CharFilter(field_name='port', lookup_expr='icontains', )

    class Meta:
        model = DataAsset
        fields = 'uir', 'name', 'url', 'host', 'port', 'comment',


class DataModelFilter(django_filters.FilterSet):
    """Фильтрация моделей данных."""

    name = CharFilter(field_name='name', lookup_expr='icontains', )
    comment = CharFilter(field_name='comment', lookup_expr='icontains', )

    class Meta:
        model = DataModel
        fields = 'name', 'comment',


class DataAssetGroupFilter(django_filters.FilterSet):
    """Фильтрация моделей данных."""

    name = CharFilter(field_name='name', lookup_expr='icontains', )
    description = CharFilter(field_name='description', lookup_expr='icontains', )

    class Meta:
        model = DataAssetGroup
        fields = 'name', 'description',
