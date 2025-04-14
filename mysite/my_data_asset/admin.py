from django.contrib import admin

from .models import (
    DataAsset, DataAssetType, DataAssetStatus,
    DataModel,
    DataTable,
    DataValue,
    DataAssetGroup, DataAssetGroupAsset, AssetStat,
)

class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        # Если объект уже существует, делаем поля readonly
        if obj:
            return self.readonly_fields
        return self.readonly_fields



@admin.register(DataAssetType)
class DataAssetTypeAdmin(BaseAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


@admin.register(DataAssetStatus)
class DataAssetStatusAdmin(BaseAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


@admin.register(DataAsset)
class DataAssetAdmin(BaseAdmin):
    list_display = 'created_at', 'name', 'is_active', 'hash_address',
    list_display_links = 'created_at', 'name', 'is_active', 'hash_address',
    search_fields = 'hash_address', 'name',
    autocomplete_fields = 'type',


@admin.register(AssetStat)
class AssetStatAdmin(BaseAdmin):
    list_display = 'get_uir', 'date_last', 'row_last', 'row_actual', 'version', 'control_1', 'control_2',
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
@admin.register(DataAssetGroup)
class DataAssetGroupsAdmin(BaseAdmin):
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
