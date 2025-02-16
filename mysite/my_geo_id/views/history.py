# import datetime
#
# from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import extend_schema
#
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
#
# from ..models import GeoObject, GeoObjectMap
# from ..serializers import GeoObjectHistorySerializer, GeoObjectMapHistorySerializer
# from rest_framework import filters
#
#
# @extend_schema(description='GeoObjectHistoryViewSet', methods=['get'])
# class GeoObjectHistoryViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     01 Название геобъекта - история изменений гео объектов
#     """
#     queryset = GeoObject.history.all()
#     serializer_class = GeoObjectHistorySerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
#
#     filterset_fields = {'object_code': ['in'], 'history_date': ['exact', ]}
#     search_fields = ['object_code', 'object_name', ]
#     ordering_fields = ['object_code', 'object_name', 'history_date']
#
#     http_method_names = ['get']  # получить только get
#
#     # @extend_schema(
#     #     summary='получить историю объекта по code',
#     #     methods=['get'],
#     # )
#     # def retrieve(self, *args, **kwargs):
#     #     return super().retrieve(*args, **kwargs)
#
#     @extend_schema(
#         summary='получить список объектов на дату',
#         methods=['get'],
#     )
#     def list(self, request, *args, **kwargs):
#         date = request.query_params.get('history_date')
#         if date:
#             date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
#             queryset = GeoObject.history.as_of(date)
#             latest_objects = {}
#             for obj in queryset:
#                 if (obj.object_code not in latest_objects
#                         or obj.history_date > latest_objects[obj.object_code].history_date):
#                     latest_objects[obj.object_code] = obj
#             serializer = self.get_serializer(list(latest_objects.values()), many=True)
#             return Response(serializer.data)
#         else:
#             return super().list(request, *args, **kwargs)
#
#
# @extend_schema(description='GeoObjectMapHistoryViewSet', methods=['get'])
# class GeoObjectMapHistoryViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     01 Название геобъекта - история изменений гео объектов
#     """
#     queryset = GeoObjectMap.history.all()
#     serializer_class = GeoObjectMapHistorySerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ]
#
#     filterset_fields = {'main': ['in'], 'history_date': ['exact', ]}
#     search_fields = ['main', 'sub', ]
#     ordering_fields = ['main', 'sub', ]
#
#     http_method_names = ['get']  # получить только get
#
#     @extend_schema(
#         summary='получить список объектов на дату',
#         methods=['get'],
#     )
#     def list(self, request, *args, **kwargs):
#         date = request.query_params.get('history_date')
#         if date:
#             date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
#             queryset = GeoObjectMap.history.as_of(date)
#             latest_objects = {}
#             for obj in queryset:
#                 if (obj.main not in latest_objects
#                         or obj.history_date > latest_objects[obj.main].history_date):
#                     latest_objects[obj.main] = obj
#             serializer = self.get_serializer(list(latest_objects.values()), many=True)
#             return Response(serializer.data)
#         else:
#             return super().list(request, *args, **kwargs)
