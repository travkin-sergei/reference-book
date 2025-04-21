import django_filters
from django_filters import CharFilter, ModelChoiceFilter
from .models import (
    DataModel,
    Asset,
    AssetStat,
    AssetGroup,
    AssetDomain,
)

# filters.py
class AssetDomainFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    link = CharFilter(field_name='link', lookup_expr='icontains')

    class Meta:
        model = AssetDomain
        fields = ['name', 'description', 'link']


class AssetFilter(django_filters.FilterSet):
    """Фильтрация источников данных."""

    type = CharFilter(field_name='type', lookup_expr='icontains', )
    domain = ModelChoiceFilter(
        queryset=AssetDomain.objects.all(),
        field_name='domain'
    )
    details = CharFilter(field_name='details', lookup_expr='icontains', )
    version = CharFilter(field_name='version', lookup_expr='icontains', )
    link = CharFilter(field_name='link', lookup_expr='icontains', )

    class Meta:
        model = Asset
        fields = 'type', 'domain', 'details', 'version', 'link',


class DataModelFilter(django_filters.FilterSet):
    """Фильтрация моделей данных."""

    name = CharFilter(field_name='name', lookup_expr='icontains', )
    comment = CharFilter(field_name='comment', lookup_expr='icontains', )

    class Meta:
        model = DataModel
        fields = 'name', 'comment',


class AssetGroupFilter(django_filters.FilterSet):
    """Фильтрация моделей данных."""

    name = CharFilter(field_name='name', lookup_expr='icontains', )
    description = CharFilter(field_name='description', lookup_expr='icontains', )

    class Meta:
        model = AssetGroup
        fields = 'name', 'description',


class AssetStatFilter(django_filters.FilterSet):
    """Фильтрация моделей данных."""

    uir = CharFilter(field_name='uir__uir', lookup_expr='icontains', )  # Замените 'name' на нужное поле

    class Meta:
        model = AssetStat
        fields = 'uir',
