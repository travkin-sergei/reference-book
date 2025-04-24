from django.apps import apps

class MultiSchemaRouter:
    # Функция для получения схемы для данного приложения
    def _get_schema_name(self, app_label):
        config = apps.get_app_config(app_label)
        return getattr(config, 'schema_name', 'public')  # Возвращает схему, или 'public' по умолчанию

    # Чтение из базы данных — направлять в нужную схему
    def db_for_read(self, model, **hints):
        schema = self._get_schema_name(model._meta.app_label)
        return schema

    # Запись в базу данных — направлять в нужную схему
    def db_for_write(self, model, **hints):
        schema = self._get_schema_name(model._meta.app_label)
        return schema

    # Разрешаем миграции для заданной схемы
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        schema = self._get_schema_name(app_label)
        if schema == 'django_system_tables' and db == 'default':
            return True  # Миграции для системных таблиц
        if schema == 'my_geo_id' and db == 'default':
            return True  # Миграции для приложения my_geo_id
        if schema == 'my_data_asset' and db == 'default':
            return True  # Миграции для приложения my_data_asset
        return False  # По умолчанию миграции не разрешены для других схем
