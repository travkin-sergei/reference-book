from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')), # Редактор текста

    path('api/v1/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('asset/', include('my_data_asset.urls')),  # Приложение Источники данных
    path('', include('my_geo_id.urls')),  # Приложение GEO-ID

]
