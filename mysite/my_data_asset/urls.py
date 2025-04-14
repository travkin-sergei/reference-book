from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .view.v1 import DataAssetAPIViewSet
from .view.web import (
    AboutAppView,
    DataAssetView, DataAssetDetailView,
    DataModelView, DataModelDetailView,
    DataTableView, DataTableDetailView,
    DataAssetGroupsView, DataAssetGroupsDetailView,
    AssetStatListView, AssetStatDetailView,
)

app_name = 'my_data_asset'
router = DefaultRouter()
router.register("data-assets", DataAssetAPIViewSet)

urlpatterns = [
    # тестирование
    path('test/', DataAssetGroupsView.as_view(), name='test'),
    # API
    path('v1/api/', include(router.urls)),
    # WEB
    path('', AboutAppView.as_view(), name='about-app'),
    # Источники данных
    path('assets/', DataAssetView.as_view(), name='data-asset'),
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
