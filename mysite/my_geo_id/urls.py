from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AboutAppView,
    ObjectCodeView,
    # представление в виде web-страницы
    ObjectView, ObjectCodeDetailView,
    ObjectMapView, ObjectMapDetailView,
    SynonymViewSet,
    ObjectMapSubViewSet, ObjectSearchView, GetGeoIdForSynonym, GeoInfoListView, ObjectDetailView, index,
    # история
    # ObjectHistoryViewSet,
    # ObjectMapHistoryViewSet,
)

app_name = 'my_geo_id'

geo_object = DefaultRouter()

geo_object.register("geo", SynonymViewSet)  # 01 Название геобъекта
geo_object.register(r'geo-maps-subs', ObjectMapSubViewSet)

urlpatterns = [

    path('api/v1/', include(geo_object.urls), name="geo"),
    path('', AboutAppView.as_view(), name='about-app'),
    # Список названий
    path('geo-id-search/', GetGeoIdForSynonym.as_view(), name='geo-id-search'),

    # Список геообъектов
    path('geo/', ObjectView.as_view(), name="geo-list"),
    path('geo/<str:pk>', ObjectDetailView.as_view(), name="geo-detail"),

    # Группировки
    path('geo-map/', ObjectMapView.as_view(), name="geo-mapp"),
    path('geo-map/<int:pk>/', ObjectMapDetailView.as_view(), name='geo-map-detail'),
    # Справочники
    path('geo-country-list/', ObjectCodeView.as_view(), name='geo-country-list'),
    path('geo-country-list/<int:pk>/', ObjectCodeDetailView.as_view(), name='geo-country-list-detail'),
    # Тестировние карты.
    path('geo-code/map/', GeoInfoListView.as_view(), name='geo-code-detail'),
    path('map/', index, name='geo-map'),

]
