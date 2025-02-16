from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AboutAppView,
    GeoObjectCodeView,
    # представление в виде web-страницы
    GeoObjectView, GeoObjectCodeDetailView,
    GeoObjectMapView, GeoObjectMapDetailView,
    GeoNamesView, GeoNamesDetailView,
    GeoNamesViewSet,
    GeoObjectMapSubViewSet, GeoObjectSearchView, GetGeoIdForGeoNames, GeoInfoListView, GeoObjectDetailView,
    # история
    # GeoObjectHistoryViewSet,
    # GeoObjectMapHistoryViewSet,

)

app_name = 'my_geo_id'

geo_object = DefaultRouter()

geo_object.register("geo", GeoNamesViewSet)  # 01 Название геобъекта
geo_object.register(r'geo-maps-subs', GeoObjectMapSubViewSet)

urlpatterns = [

    path('api/v1/', include(geo_object.urls), name="geo"),
    path('', AboutAppView.as_view(), name='about-app'),
    # Список названий
    path('geo-id-search/', GetGeoIdForGeoNames.as_view(), name='geo-id-search'),
    path('geo-name/', GeoNamesView.as_view(), name='geo-name'),
    path('geo-name/<str:pk>/', GeoNamesDetailView.as_view(), name='geo-name-detail'),

    # Список геообъектов
    path('geo/', GeoObjectView.as_view(), name="geo-list"),
    path('geo/<str:pk>', GeoObjectDetailView.as_view(), name="geo-detail"),

    # Группировки
    path('geo-map/', GeoObjectMapView.as_view(), name="geo-map"),
    path('geo-map/<int:pk>/', GeoObjectMapDetailView.as_view(), name='geo-map-detail'),
    # Справочники
    path('geo-code/', GeoObjectCodeView.as_view(), name='geo-code'),
    path('geo-code/<int:pk>/', GeoObjectCodeDetailView.as_view(), name='geo-code-detail'),
    # Тестировние карты.
    path('geo-code/map/', GeoInfoListView.as_view(), name='geo-code-detail'),
]
