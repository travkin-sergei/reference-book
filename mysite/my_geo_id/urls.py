from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AboutAppView,
    GeoObjectCodeView,
    # представление в виде web-страницы
    GeoObjectView, GeoObjectCodeDetailView,
    GeoObjectMapView, GeoObjectMapDetailView,
    GeoNamesViewSet,
    GeoObjectMapSubViewSet, GeoObjectSearchView, GetGeoIdForGeoNames, GeoInfoListView, GeoObjectDetailView, index,
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

    # Список геообъектов
    path('geo/', GeoObjectView.as_view(), name="geo-list"),
    path('geo/<str:pk>', GeoObjectDetailView.as_view(), name="geo-detail"),

    # Группировки
    path('geo-map/', GeoObjectMapView.as_view(), name="geo-mapp"),
    path('geo-map/<int:pk>/', GeoObjectMapDetailView.as_view(), name='geo-map-detail'),
    # Справочники
    path('geo-country-list/', GeoObjectCodeView.as_view(), name='geo-country-list'),
    path('geo-country-list/<int:pk>/', GeoObjectCodeDetailView.as_view(), name='geo-country-list-detail'),
    # Тестировние карты.
    path('geo-code/map/', GeoInfoListView.as_view(), name='geo-code-detail'),
    path('map/', index, name='geo-map'),

]
