from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q  # Импортируем Q для сложных запросов

from ..filters import (
    ObjectFilter,
    ObjectCodeFilter,
    ObjectMapFilter,
)
from ..models import (
    Object,
    ObjectCode, ObjectCodeSub,  # Справочники
    ObjectMap, ObjectMapSub, Synonym, Info, MapLocation,  # Группировки
)


# Synonym
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

    model = Info
    template_name = 'geo_object/map_all.html'
    context_object_name = 'geo_info_list'

    def get_queryset(self):
        """Фильтруем активные геообъекты."""
        result = Info.objects.filter(is_active=True)
        return result


# Список объектов
class ObjectView(ListView):
    """Список геообъектов."""

    queryset = (Object.objects.filter(is_active=True))
    template_name = "geo_object/geo.html"
    context_object_name = 'geo_objects'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = ObjectFilter(self.request.GET, queryset=queryset)  # Инициализируем фильтр
        return self.filter.qs

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter  #
        return context


class ObjectDetailView(DetailView):
    """Список геообъектов."""

    queryset = (Object.objects.filter(is_active=True))
    template_name = "geo_object/geo-detail.html"
    context_object_name = 'geo_objects_detail'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        """Добавляем связанные Synonym в контекст."""
        context = super().get_context_data(**kwargs)
        geo_object = self.object  # Получаем текущий объект Object
        context['names'] = geo_object.name.all()  # Получаем все связанные Synonym
        context['info'] = geo_object.info  # Получаем все связанные Synonym
        return context


# Справочники
class ObjectCodeView(ListView):
    """Представление для отображения списка ObjectCode."""

    queryset = ObjectCode.objects.filter(is_active=True)
    template_name = 'geo_object/country-list.html'
    context_object_name = 'geo_object_code'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = ObjectCodeFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


# Справочники
class ObjectCodeDetailView(DetailView):
    """
    Представление для отображения деталей кода геообъекта.
    1) Значания в рамках справочника долны быть разделены на:
        1.1) уникальные площади
        1.2) сграуппированные
    """

    queryset = (
        ObjectCode
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
            ObjectCodeSub
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
class ObjectMapView(ListView):
    """Представление для отображения списка ObjectCode."""

    queryset = ObjectMap.objects.filter(is_active=True)
    template_name = 'geo_object/geo-map.html'
    context_object_name = 'geo_object_map'

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = ObjectMapFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


# Группировки
class ObjectMapDetailView(DetailView):
    """Представление для отображения деталей ObjectMap."""

    model = ObjectMap  # Указываем модель, для которой будет отображаться детальная информация
    template_name = 'geo_object/geo-map-detail.html'  # Шаблон для отображения деталей
    context_object_name = 'geo_object_map'  # Имя контекста для доступа к объекту в шаблоне

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        # Получаем только активные объекты
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные в контекст."""

        context = super().get_context_data(**kwargs)

        geo_object_map = self.object  # Получаем текущий объект ObjectMap
        related_objects = geo_object_map.sub_objects.all()  # Получаем связанные объекты, если они есть
        context['related_objects'] = related_objects if related_objects.exists() else None
        return context


class SynonymTView(ListView):
    queryset = (
        Synonym
        .objects.filter(is_active=True)
    )
    context_object_name = 'geo_name'
    template_name = "geo_object/geo-name.html"
    paginate_by = 20


class GetGeoIdForSynonym(ListView):
    """Поисковик по синонимам, для поиска GEO-ID"""

    model = Object
    context_object_name = 'geo_objects'
    template_name = "geo_object/geo-id-search.html"
    paginate_by = 20

    def get_queryset(self):
        # Получаем имя из GET-параметров
        self.name = self.request.GET.get('name', None)
        if self.name:
            self.name = self.name.strip()
            # Ищем синонимы по имени
            synonyms = Synonym.objects.filter(
                name__icontains=self.name
            ).values_list('geo_id', flat=True)  # Получаем geo_id из найденных синонимов

            # Теперь ищем объекты Object по найденным geo_id
            return Object.objects.filter(
                object_code__in=synonyms,  # Предполагается, что geo_id соответствует object_code
                is_active=True
            ).prefetch_related('name')

        # Возвращаем пустой queryset, если имя не указано
        return Object.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.name
        return context


def index(request):
    return render(request, 'geo_object/map.html', )
