from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView

from ..filters import (
    GeoObjectFilter,
    GeoObjectCodeFilter,
    GeoObjectMapFilter,
)
from ..models import (
    GeoObject,
    GeoObjectCode, GeoObjectCodeSub,  # Справочники
    GeoObjectMap, GeoObjectMapSub, GeoNames, GeoInfo, MapLocation,  # Группировки
)


# О приложении
class AboutAppView(TemplateView):
    """
    Отображение информации о текущем приложении из шаблона приложения.
    Каждое приложение должно иметь стандартное описание в HTML.
    """

    template_name = 'geo_object/about-application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GeoInfoListView(ListView):
    """Отображение списка геообъектов с дополнительной информацией."""

    model = GeoInfo
    template_name = 'geo_object/map_all.html'
    context_object_name = 'geo_info_list'

    def get_queryset(self):
        """Фильтруем активные геообъекты."""
        result = GeoInfo.objects.filter(is_active=True)
        return result


# Список объектов
class GeoObjectView(ListView):
    """Список геообъектов."""

    queryset = (GeoObject.objects.filter(is_active=True))
    template_name = "geo_object/geo.html"
    context_object_name = 'geo_objects'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = GeoObjectFilter(self.request.GET, queryset=queryset)  # Инициализируем фильтр
        return self.filter.qs

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter  #
        return context


class GeoObjectDetailView(DetailView):
    """Список геообъектов."""

    queryset = (GeoObject.objects.filter(is_active=True))
    template_name = "geo_object/geo-detail.html"
    context_object_name = 'geo_objects_detail'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """Добавляем связанные GeoNames в контекст."""
        context = super().get_context_data(**kwargs)
        geo_object = self.object  # Получаем текущий объект GeoObject
        context['geo_names'] = geo_object.geo_name.all()  # Получаем все связанные GeoNames
        context['geo_info'] = geo_object.geo_info  # Получаем все связанные GeoNames
        return context


# Справочники
class GeoObjectCodeView(ListView):
    """Представление для отображения списка GeoObjectCode."""

    queryset = (
        GeoObjectCode
        .objects.filter(is_active=True)
    )
    template_name = 'geo_object/country-list.html'
    context_object_name = 'geo_object_code'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = GeoObjectCodeFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


# Справочники
class GeoObjectCodeDetailView(DetailView):
    """
    Представление для отображения деталей кода геообъекта.
    1) Значания в рамках справочника долны быть разделены на:
        1.1) уникальные площади
        1.2) сграуппированные
    """

    queryset = (
        GeoObjectCode
        .objects
        .filter(is_active=True)
    )
    template_name = 'geo_object/country-list-detail.html'
    context_object_name = 'geo_object_code'

    def get_context_data(self, **kwargs):
        """Добавляем связанные объекты в контекст."""
        context = super().get_context_data(**kwargs)
        # Получаем связанные объекты из промежуточной модели
        related_objects = (
            GeoObjectCodeSub
            .objects.filter(geo_object_code=self.object)
            .order_by("is_group")  # 1.1.
        )

        # Настраиваем пагинацию для связанных объектов
        paginator = Paginator(related_objects, 500)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['related_objects'] = page_obj
        return context


# Группировки
class GeoObjectMapView(ListView):
    """Представление для отображения списка GeoObjectCode."""

    queryset = GeoObjectMap.objects.filter(is_active=True)
    template_name = 'geo_object/geo-map.html'
    context_object_name = 'geo_object_map'

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = GeoObjectMapFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


# Группировки
class GeoObjectMapDetailView(DetailView):
    """Представление для отображения деталей GeoObjectMap."""

    model = GeoObjectMap  # Указываем модель, для которой будет отображаться детальная информация
    template_name = 'geo_object/geo-map-detail.html'  # Шаблон для отображения деталей
    context_object_name = 'geo_object_map'  # Имя контекста для доступа к объекту в шаблоне

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        # Получаем только активные объекты
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные в контекст."""

        context = super().get_context_data(**kwargs)

        geo_object_map = self.object  # Получаем текущий объект GeoObjectMap
        related_objects = geo_object_map.sub_objects.all()  # Получаем связанные объекты, если они есть
        context['related_objects'] = related_objects if related_objects.exists() else None
        return context


class GeoNamesTView(ListView):
    queryset = (
        GeoNames
        .objects.filter(is_active=True)
    )
    context_object_name = 'geo_name'
    template_name = "geo_object/geo-name.html"
    paginate_by = 20


class GetGeoIdForGeoNames(ListView):
    """Поисковик по синонимам, для поиска GEO-ID"""

    model = GeoObject
    context_object_name = 'geo_objects'
    template_name = "geo_object/geo-id-search.html"
    paginate_by = 20

    def get_queryset(self):
        # Получаем имя из GET-параметров
        self.geo_name = self.request.GET.get('name', None)
        if self.geo_name:
            self.geo_name = self.geo_name.strip()
            # Фильтруем объекты GeoObject по имени GeoNames
            return GeoObject.objects.filter(
                geo_name__name__icontains=self.geo_name,  # Используем icontains для нечувствительного к регистру поиска
                is_active=True
            ).prefetch_related('geo_name')
        # Возвращаем пустой queryset, если имя не указано
        return GeoObject.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['geo_name'] = self.geo_name
        return context


def index(request):
    return render(request, 'geo_object/map.html', )
