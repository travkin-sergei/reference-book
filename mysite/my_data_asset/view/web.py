from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,

)

from ..filters import (
    DataAssetFilter,
    DataModelFilter, DataAssetGroupFilter,
)
from ..models import (
    DataAsset,
    DataModel,
    DataTable,
    DataValue, DataAssetGroup, DataAssetGroupAsset,
)


class AboutAppView(TemplateView):
    """
    Отображение информации о текущем приложении из шаблона приложения.
    Каждое приложение должно иметь стандартное описание в HTML.
    """

    template_name = 'my_data_asset/about_application.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DataAssetView(ListView):
    """Отображение списка источников данных с возможностью фильтрации данных на web странице."""

    template_name = 'my_data_asset/data-asset.html'
    queryset = DataAsset.objects.filter(is_active=True)
    context_object_name = 'data_assets'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = DataAssetFilter(self.request.GET, queryset=queryset)  # Инициализируем фильтр
        return self.filter.qs  # Возвращаем отфильтрованный queryset

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class DataAssetDetailView(DetailView):
    """Представление для отображения деталей источника данных."""

    queryset = DataAsset.objects.filter(is_active=True)
    template_name = 'my_data_asset/data-asset-detail.html'
    context_object_name = 'data_asset_detail'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем текущий объект DataAsset
        data_asset = self.object
        # Получаем все связанные DataModel
        data_models = DataModel.objects.filter(data_asset=data_asset, is_active=True)

        # Пагинация
        paginator = Paginator(data_models, 20)  # Показывать 20 моделей на странице
        page_number = self.request.GET.get('page')  # Получаем номер страницы из GET-запроса
        page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

        context['page_obj'] = page_obj  # Передаем объекты страницы в контекст
        return context


class DataModelView(ListView):
    """Отображение списка моделей данных с возможностью фильтрации данных на web странице."""

    template_name = 'my_data_asset/data-model.html'
    context_object_name = 'data_model'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = DataModel.objects.filter(is_active=True)  # Фильтруем только активные модели
        self.filter = DataModelFilter(self.request.GET, queryset=queryset)  # Инициализируем фильтр
        return self.filter.qs  # Возвращаем отфильтрованный queryset

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class DataModelDetailView(DetailView):
    """Представление для отображения деталей моделей данных."""

    template_name = 'my_data_asset/data-model-detail.html'
    context_object_name = 'data_model_detail'
    queryset = DataModel.objects.filter(is_active=True)

    def get_object(self, queryset=None):
        """Получаем объект DataModel, фильтруя по is_active."""
        obj = super().get_object(queryset)
        if not obj.is_active:
            raise Http404("Модель данных не активна.")
        return obj

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем текущий объект DataModel
        data_model = self.object

        # Получаем все связанные DataTable, фильтруя по is_active
        related_data_tables = DataTable.objects.filter(data_model=data_model, is_active=True)

        # Пагинация
        paginator = Paginator(related_data_tables, 20)  # Показывать 20 таблиц на странице
        page_number = self.request.GET.get('page')  # Получаем номер страницы из GET-запроса
        page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

        context['page_obj'] = page_obj  # Передаем объекты страницы в контекст
        return context


class DataTableView(ListView):
    """Отображение списка моделей данных с возможностью фильтрации данных на web странице."""

    template_name = 'my_data_asset/data-model.html'
    queryset = DataTable.objects.filter(is_active=True)
    context_object_name = 'data_model'
    paginate_by = 20

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = DataModelFilter(self.request.GET, queryset=queryset)  # Инициализируем фильтр
        return self.filter.qs  # Возвращаем отфильтрованный queryset

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class DataTableDetailView(DetailView):
    """Представление для отображения деталей таблицы данных."""

    queryset = DataTable.objects.filter(is_active=True)

    template_name = 'my_data_asset/data-table-detail.html'
    context_object_name = 'data_table_detail'

    def get_context_data(self, **kwargs):
        # Получаем контекст из родительского класса
        context = super().get_context_data(**kwargs)
        # Получаем текущий объект DataTable
        data_table = self.object

        # Получаем все связанные DataValue, фильтруя по is_active
        related_data_values = DataValue.objects.filter(data_table=data_table, is_active=True)

        # Пагинация
        paginator = Paginator(related_data_values, 20)  # Показывать 20 значений на странице
        page_number = self.request.GET.get('page')  # Получаем номер страницы из GET-запроса
        page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

        context['page_obj'] = page_obj  # Передаем объекты страницы в контекст
        return context


class DataAssetGroupsView(ListView):
    """Отображение групп источников данных."""

    queryset = DataAssetGroup.objects.filter(is_active=True)
    template_name = 'my_data_asset/data-asset-groups.html'
    context_object_name = 'data_asset_groups'

    def get_queryset(self):
        """Фильтруем queryset на основе параметров запроса."""
        queryset = super().get_queryset()
        self.filter = DataAssetGroupFilter(self.request.GET, queryset=queryset)  # Инициализируем фильтр
        return self.filter.qs  # Возвращаем отфильтрованный queryset

    def get_context_data(self, **kwargs):
        """Добавляем фильтр в контекст."""
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class DataAssetGroupsDetailView(DetailView):
    """Отображение групп источников данных."""

    queryset = DataAssetGroup.objects.filter(is_active=True)  # Убедитесь, что это правильная модель
    template_name = 'my_data_asset/data-asset-groups-detail.html'
    context_object_name = 'data_asset_group'

    def get_context_data(self, **kwargs):
        """Добавляем источники данных в контекст."""
        context = super().get_context_data(**kwargs)
        group_asset = self.object  # Получаем текущую группу источников данных

        # Получаем все связанные источники данных через related_name
        data_assets = DataAssetGroupAsset.objects.filter(
            name=group_asset)  # Убедитесь, что group_asset - это экземпляр DataAssetGroup

        context['data_assets'] = data_assets  # Передаем все источники данных в контекст
        return context

