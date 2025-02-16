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


# views.py
# views.py
from django.shortcuts import render
import networkx as nx
import plotly.graph_objects as go
from django.apps import apps


def dependency_graph(request, app_label):
    try:
        # Получаем конфигурацию приложения
        app_config = apps.get_app_config(app_label)
    except LookupError:
        # Если приложение не найдено, возвращаем ошибку 404
        return HttpResponse(f"Приложение '{app_label}' не найдено", status=404)

    # Получаем все модели из этого приложения
    models = app_config.get_models()

    # Создаем граф
    G = nx.DiGraph()

    # Добавляем узлы и ребра в граф
    for model in models:
        model_name = model.__name__
        G.add_node(model_name)

        # Проверяем связи ForeignKey, OneToOneField и ManyToManyField
        for field in model._meta.get_fields():
            if field.is_relation:
                related_model = field.related_model
                # Добавляем связь только если связанная модель тоже принадлежит этому приложению
                if related_model in models:
                    related_model_name = related_model.__name__
                    G.add_edge(model_name, related_model_name)

    # Создаем позиции узлов для визуализации
    pos = nx.spring_layout(G)

    # Создаем данные для Plotly
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'))

    node_trace = go.Scatter(
        x=[], y=[], text=[], mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
            )
        )
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)

    # Создаем фигуру
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    # Конвертируем фигуру в HTML
    graph_html = fig.to_html(full_html=False)

    # Передаем HTML в шаблон
    return render(request, 'my_data_asset/dependency_graph.html', {'graph_html': graph_html})



from django.shortcuts import render, HttpResponse
import plotly.graph_objects as go
import json


def custom_world_map(request):
    try:
        # Загрузка GeoJSON файла
        with open(
                r'C:\Users\travk\OneDrive\Desktop\Новая папка (2)\Новая папка\custom_countries.geojson'
                , 'r'
                , encoding='utf-8'
        ) as f:
            geojson_data = json.load(f)

        # Пример данных для каждой страны
        data = {
            "Страна": ["Россия", "США"],
            "Значение": [145, 330]
        }

        # Создаем карту с пользовательскими границами
        fig = go.Figure(go.Choroplethmapbox(
            geojson=geojson_data,  # Ваш GeoJSON файл
            locations=data["Страна"],  # Названия стран
            z=data["Значение"],  # Данные для визуализации
            featureidkey="properties.name",  # Ключ для сопоставления данных с GeoJSON
            colorscale="Viridis",  # Цветовая шкала
            marker_opacity=0.5,
            marker_line_width=0
        ))

        # Настройка макета карты
        fig.update_layout(
            mapbox_style="carto-positron",  # Стиль карты
            mapbox_zoom=1,  # Масштаб
            mapbox_center={"lat": 50, "lon": 0},  # Центр карты
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )

        # Конвертируем карту в HTML
        map_html = fig.to_html(full_html=False)

        # Передаем HTML в шаблон
        return render(request, 'my_data_asset/map.html', {'map_html': map_html})

    except FileNotFoundError:
        return HttpResponse("Файл GeoJSON не найден", status=404)
    except json.JSONDecodeError:
        return HttpResponse("Ошибка при чтении GeoJSON файла", status=400)
    except Exception as e:
        return HttpResponse(f"Произошла ошибка: {str(e)}", status=500)
