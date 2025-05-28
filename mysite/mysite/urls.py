from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Административная панель
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),  # Редактор текста
    # API
    path('api/v1/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Токены авторизации
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение access и refresh токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление access токена
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Проверка валидности токена
    # Приложения
    path('auth/', include('my_auth.urls', namespace='my_auth')),
    path('asset/', include('my_data_asset.urls')),  # Приложение Источники данных
    path('', include('my_geo_id.urls')),  # Приложение GEO-ID
]
