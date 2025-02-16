from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .view.v1 import DataAssetAPIViewSet
from .view.web import (
    AboutAppView,
    DataAssetView, DataAssetDetailView,
    DataModelView, DataModelDetailView,
    DataTableView, DataTableDetailView,
    DataAssetGroupsView, DataAssetGroupsDetailView, dependency_graph, custom_world_map,
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
    path('data-assets/', DataAssetView.as_view(), name='data-asset'),
    path('data-assets/<int:pk>/', DataAssetDetailView.as_view(), name='data-asset-detail'),
    # Модели источников данных
    path('data-model/', DataModelView.as_view(), name='data-model'),
    path('data-model/<int:pk>/', DataModelDetailView.as_view(), name='data-model-detail'),
    # Модели таблиц данных
    path('data-table/', DataTableView.as_view(), name='data-table'),
    path('data-table/<int:pk>/', DataTableDetailView.as_view(), name='data-table-detail'),
    # Группировка источников данных
    path('data-assets-groups/', DataAssetGroupsView.as_view(), name='data-asset-groups'),
    path('data-assets-groups/<int:pk>/', DataAssetGroupsDetailView.as_view(), name='data-asset-groups-detail'),

    path('dependency-graph/', dependency_graph, name='dependency_graph'),
    path('dependency-graph/<str:app_label>/', dependency_graph, name='dependency_graph'),
    # Map
    path('world-map/', custom_world_map, name='world_map'),
]
