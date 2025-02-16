from django.contrib import admin

from .models import (
    DataAsset, DataAssetType, DataAssetStatus,
    DataModel,
    DataTable,
    DataValue,
    DataAssetGroup, DataModelGroup, DataTableGroup, DataValueGroup, DataAssetGroupAsset,
)


@admin.register(DataAssetType)
class DataAssetTypeAdmin(admin.ModelAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


@admin.register(DataAssetStatus)
class DataAssetStatusAdmin(admin.ModelAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


@admin.register(DataAsset)
class DataAssetAdmin(admin.ModelAdmin):
    list_display = 'created_at', 'name', 'is_active', 'hash_address',
    list_display_links = 'created_at', 'name', 'is_active', 'hash_address',
    search_fields = 'hash_address', 'name',
    autocomplete_fields = 'type', 'status',


@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):
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
class DataTableAdmin(admin.ModelAdmin):
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
class DataValueAdmin(admin.ModelAdmin):
    list_display = 'updated_at', 'is_active', 'hash_address', 'data_table', 'name',
    list_display_links = 'updated_at', 'is_active', 'hash_address',
    search_fields = 'hash_address', 'name', 'data_table__name', 'name',
    autocomplete_fields = 'data_table', 'parent',


# =============================================== Группировки источников ===============================================
@admin.register(DataAssetGroup)
class DataAssetGroupsAdmin(admin.ModelAdmin):
    """Отображение группировок Моделей данных"""

    list_display = 'is_active', 'name',  # 'data_asset_group_verbose',
    list_display_links = 'is_active', 'name',  # 'data_asset_group_verbose',
    list_filter = 'name',
    search_fields = 'name',


@admin.register(DataAssetGroupAsset)
class DataAssetGroupAssetAdmin(admin.ModelAdmin):
    """Отображение группировок Моделей данных"""

    list_display = 'created_at', 'name', 'data_assets',
    list_filter = 'name',
    search_fields = 'name__name', 'data_assets__name',
    autocomplete_fields = 'name', 'data_assets',
    list_editable = 'name', 'data_assets',
