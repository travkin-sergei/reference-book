from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .view.v1 import DataAssetAPIViewSet, AssetStatAPIViewSet
from .view.web import (
    AboutAppView,
    AssetView, DataAssetDetailView,
    DataModelView, DataModelDetailView,
    DataTableView, DataTableDetailView,
    DataAssetGroupsView, DataAssetGroupsDetailView,
    AssetStatListView, AssetStatDetailView,
    AssetDomain, AssetDomainView, DomainTablesView,
)

app_name = 'my_data_asset'
router = DefaultRouter()
router.register("assets", DataAssetAPIViewSet)
router.register("assets", AssetStatAPIViewSet)

urlpatterns = [
    # тестирование
    path('test/', DataAssetGroupsView.as_view(), name='test'),
    # API
    path('v1/api/', include(router.urls)),
    # WEB
    path('', AboutAppView.as_view(), name='about-app'),
    # Источники данных dddx
    path('asset/asset-domain/', AssetDomainView.as_view(), name='asset-domain'),
    path('asset/asset-domain/<str:domain_id>/', DomainTablesView.as_view(), name='domain-tables'),
    # Источники данных
    path('assets/', AssetView.as_view(), name='data-asset'),
    path('assets/<str:pk>/', DataAssetDetailView.as_view(), name='data-asset-detail'),
    # Статистика источников данных
    path('stat/', AssetStatListView.as_view(), name='asset-stat'),
    path('stat/<int:pk>/', AssetStatDetailView.as_view(), name='asset-stat-detail'),
    # Модели источников данных
    path('model/', DataModelView.as_view(), name='data-model'),
    path('model/<int:pk>/', DataModelDetailView.as_view(), name='data-model-detail'),
    # Модели таблиц данных
    path('table/', DataTableView.as_view(), name='data-table'),
    path('table/<int:pk>/', DataTableDetailView.as_view(), name='data-table-detail'),
    # Группировка источников данных
    path('assets-groups/', DataAssetGroupsView.as_view(), name='data-asset-groups'),
    path('assets-groups/<int:pk>/', DataAssetGroupsDetailView.as_view(), name='data-asset-groups-detail'),
]
