from django.contrib import admin

from .models import (
    DataModel,
    DataTable,
    DataValue,
    AssetGroup, DataAssetGroupAsset,
    AssetStat,
    Asset, AssetType, AssetDomain, AssetDetails, AssetVersion,
)


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        # Если объект уже существует, делаем поля readonly
        if obj:
            return self.readonly_fields
        return self.readonly_fields


@admin.register(AssetType)
class AssetTypeAdmin(BaseAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


@admin.register(AssetStat)
class AssetStatAdmin(BaseAdmin):
    list_display = 'get_uir', 'date_last', 'version', 'control_1', 'control_2',
    list_display_links = 'get_uir', 'date_last',
    search_fields = 'uir__uir', 'version',
    autocomplete_fields = 'uir',

    def get_uir(self, obj):
        return obj.uir.uir

    get_uir.short_description = 'УИР'


@admin.register(DataModel)
class DataModelAdmin(BaseAdmin):
    list_display = 'created_at', 'name', 'is_active', 'hash_address',
    list_display_links = 'created_at', 'name', 'is_active', 'hash_address',
    search_fields = 'hash_address', 'data_asset__name', 'name',
    autocomplete_fields = 'data_asset',


class DataValueInline(admin.TabularInline):
    """
    Inline для редактирования дополнительной информации о геообъекте.
    - Каждая строка должна быть строкой в админке.
    - имеется ограничение на передачу количества строк (максимальный размер пока неизвестен).
    """

    model = DataValue
    search_fields = 'hash_address', 'name', 'data_table__name', 'name',
    autocomplete_fields = 'data_table', 'parent',
    extra = 10


@admin.register(DataTable)
class DataTableAdmin(BaseAdmin):
    """
    Заполнение таблицы данных и данных о столбцах этой таблице.
    inlines к DataValueInline:
        - Каждая строка должна быть строкой в админке.
        - Имеется ограничение на передачу количества строк (максимальный размер пока неизвестен).
    """
    inlines = [DataValueInline]

    list_display = 'created_at', 'name', 'is_active', 'hash_address',
    list_display_links = 'created_at', 'name', 'is_active', 'hash_address',
    search_fields = 'hash_address', 'data_model__name', 'name',
    autocomplete_fields = 'data_model',


# 04 Значения таблицы
@admin.register(DataValue)
class DataValueAdmin(BaseAdmin):
    list_display = 'updated_at', 'is_active', 'hash_address', 'data_table', 'name',
    list_display_links = 'updated_at', 'is_active', 'hash_address',
    search_fields = 'hash_address', 'name', 'data_table__name', 'name',
    autocomplete_fields = 'data_table', 'parent',


# =============================================== Группировки источников ===============================================
@admin.register(AssetGroup)
class AssetGroupsAdmin(BaseAdmin):
    """Отображение группировок Моделей данных"""

    list_display = 'is_active', 'name',  # 'data_asset_group_verbose',
    list_display_links = 'is_active', 'name',  # 'data_asset_group_verbose',
    list_filter = 'name',
    search_fields = 'name',


@admin.register(DataAssetGroupAsset)
class DataAssetGroupAssetAdmin(BaseAdmin):
    """Отображение группировок Моделей данных"""

    list_display = 'created_at', 'name', 'data_assets',
    list_filter = 'name',
    search_fields = 'name__name', 'data_assets__name',
    autocomplete_fields = 'name', 'data_assets',
    list_editable = 'name', 'data_assets',


class AssetTypeInline(admin.TabularInline):
    model = AssetType
    fields = 'name',  # Указываем только необходимые поля
    extra = 1


@admin.register(AssetDomain)
class AssetDomainAdmin(BaseAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


class AssetDomainInline(admin.TabularInline):
    model = AssetDomain
    fields = 'name',  # Указываем только необходимые поля
    extra = 1


@admin.register(AssetDetails)
class AssetDetailsAdmin(BaseAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


class AssetDetailsInline(admin.TabularInline):
    model = AssetDetails
    fields = 'name',  # Указываем только необходимые поля
    extra = 1


@admin.register(AssetVersion)
class AssetVersionAdmin(BaseAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


class AssetVersionInline(admin.TabularInline):
    model = AssetVersion
    fields = 'name',  # Указываем только необходимые поля
    extra = 1


@admin.register(Asset)
class AssetAdmin(BaseAdmin):
    """Источник данных."""

    list_display = 'type', 'domain', 'details', 'version', 'link', 'description',
    list_display_links = 'type', 'domain', 'details', 'version',
    search_fields = 'type__name', 'domain__name', 'details__name', 'version__name', 'link', 'description'
    autocomplete_fields = 'type', 'domain', 'details', 'version',
