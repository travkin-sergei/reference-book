from django.db import models
from ckeditor.fields import RichTextField


class SystemColumns(models.Model):
    """Набор минимальных системных столбцов."""

    created_at = models.DateTimeField(
        auto_now_add=True
        , db_comment='{"name":"Строка в базе данных создана.",}'
        , help_text="Дата создания строки в текущей базе данных.",
    )
    updated_at = models.DateTimeField(
        auto_now=True
        , db_comment='{"name":"Строка в базе данных обновлена.",}'
        , help_text="Дата обновления строки в текущей базе данных.",
    )
    is_active = models.BooleanField(
        default=True
        , db_comment='{"name":"Стока в базе данных активна.",}'
        , help_text="Является ли запись действующей на текущей момент?",
    )

    class Meta:
        abstract = True


class BaseModel(SystemColumns):
    """Базовая модель приложения DataAsset."""

    hash_address = models.CharField(
        max_length=64, blank=True, null=True
        , db_comment='{'
                     '"name":"Хеш адрес строки",'
                     '"description":"Алгоритм sha256. Важно соблюдать регистр и порядок.",'
                     '}'
        , help_text="Алгоритм sha256. Важно соблюдать регистр и порядок.",
    )
    task = models.CharField(
        max_length=64, blank=True, null=True
        , db_comment='{'
                     '"name":"Задача, в рамках которой появилась запись.",'
                     '"description":"Имеется в виду не в этой базе данных, а в источнике, если это применимо.",'
                     ',}'
        , help_text="Алгоритм sha256. Важно соблюдать регистр и порядок.",
    )

    class Meta:
        abstract = True


class DataAssetType(SystemColumns):
    """
    Справочник типов источников данных.
    Ограничение уникальность:
     - Тип источника данных.
     """

    name = models.CharField(
        max_length=255
        , db_comment='{"name":"Тип источника данных.",}'
        , help_text="Тип источника данных.",
    )

    class Meta:
        db_table = 'data_asset_type'  # Указываем имя таблицы в базе данных
        unique_together = [["name", ]]
        verbose_name = '01.1 Тип источника данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '01.1 Типы источников данных'  # Указываем имя таблицы в админке

    def __str__(self):
        return self.name or 'NO DATA'


class DataAssetStatus(SystemColumns):
    """
    Справочник статусов источников данных.
    Ограничение уникальность:
     - Статус ресурса;
    """

    name = models.CharField(
        max_length=255
        , verbose_name="Статус ресурса"
        , db_comment='{"name":"Статус ресурса.",}'
    )

    class Meta:
        db_table = 'data_asset_status'  # Указываем имя таблицы в базе данных
        unique_together = [["name", ]]
        verbose_name = '01.2 Статус источника данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '01.2 Статус источников данных'  # Указываем имя таблицы в админке

    def __str__(self):
        return self.name or 'NO DATA'


class DataAsset(BaseModel):
    """
    Список описанных источников данных.
    Ограничение уникальность:
     - Уникальный идентификатор ресурса;
    """

    type = models.ForeignKey(
        'DataAssetType', on_delete=models.CASCADE, null=True, blank=True
        , verbose_name="Тип источника данных"
        , db_comment='{"name":"Тип источника данных.",}'
        , help_text="Тип источника данных."

    )
    last_update = models.DateField(
        auto_now=True
        , verbose_name="Последнее обновление."
        , db_comment='{'
                     'name":"Последнее обновление информации об источнике", '
                     '"description":"не надо путать с обновлением строки базы данных.",'
                     '}'
        , help_text="Последнее обновление информации об источнике данных.",
    )
    uir = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="УИР."
        , db_comment='{"name":"Уникальный идентификатор ресурса",}'
        , help_text="Уникальный идентификатор ресурса.",
    )
    url = models.URLField(
        blank=True, null=True
        , verbose_name="URL."
        , db_comment='{"name":"URL ссылка.",}'
        , help_text="URL ссылка.",
    )
    status = models.ForeignKey(
        'DataAssetStatus', on_delete=models.CASCADE, null=True, blank=True
        , verbose_name="Статус"
        , db_comment='{"name":"Статус",}'
    )
    name = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Название"
        , db_comment='{"name":"Название ресурса",}'
        , help_text="Название ресурса",
    )
    comment = RichTextField(  # models.TextField
        blank=True, null=True
        , verbose_name="Комментарий"
        , db_comment='{"name":"Описание ресурса",}'
        , help_text="Описание ресурса.",
    )
    version = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Версия"
        , db_comment='{"name":"Версия ресурса.",}'
        , help_text="Версия ресурса.",
    )
    host = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Хост"
        , db_comment='{"name":"Хост.",}'
    )
    port = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Порт."
        , db_comment='{"name":"Порт",}'
    )

    class Meta:
        db_table = 'data_asset'  # Указываем имя таблицы в базе данных
        constraints = [
            models.UniqueConstraint(fields=['url'], name='unique_data_asset_url')
        ]
        ordering = ['name']  # Сортировка по дате создания (по убыванию)
        verbose_name = '01 Источник данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '01 Источники данных'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.status} - {self.name}' or 'NO DATA'


class DataModel(BaseModel):
    """
    Список описанных моделей источников данных.
    Ограничение уникальность:
     - Список описанных источников данных;
     - Название модели.
    """

    data_asset = models.ForeignKey('DataAsset', on_delete=models.CASCADE, null=True, blank=True)  # Внешний ключ
    name = models.CharField(max_length=255, blank=True, null=True)  # Схема
    comment = RichTextField(
        help_text="Комментарий.",
        blank=True, null=True
    )

    class Meta:
        db_table = 'data_model'  # Указываем имя таблицы в базе данных
        unique_together = [["data_asset", "name", ]]
        verbose_name = '02 Модель данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '02 Модели данных'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.data_asset} - {self.name}' or 'NO DATA'


class DataTable(BaseModel):
    """
    Список таблиц данных моделей.
    Ограничение уникальность:
     - Список таблиц данных моделей;
     - Тип;
     - Название.
    """

    data_model = models.ForeignKey(
        'DataModel', on_delete=models.CASCADE, null=True, blank=True
    )  # Внешний ключ
    type = models.CharField(
        max_length=255, blank=True, null=True
    )  # Тип таблицы
    name = models.CharField(
        max_length=255, blank=True, null=True
    )  # Название таблицы данных
    comment = RichTextField(
        blank=True, null=True
        , help_text="Комментарий."
    )

    class Meta:
        db_table = 'data_table'  # Указываем имя таблицы в базе данных
        unique_together = [["data_model", "type", "name", ]]
        verbose_name = '03 Таблица данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '03 Таблицы данных'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.data_model} - {self.type} - {self.name}' or 'NO DATA'


class DataValue(BaseModel):
    """
    Содержит список полей источников данных.
    Ограничение уникальность:
     - Список таблиц данных моделей;
     - Название.
    """

    data_table = models.ForeignKey(
        'DataTable', on_delete=models.CASCADE, null=True, blank=True
        , verbose_name="Список таблиц данных моделей."
        , db_comment='{"name":"Список таблиц данных моделей.",}'
        , help_text="Список таблиц данных моделей.",
    )
    name = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Название"
        , db_comment='{"name":"Название",}'
        , help_text="Название",
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True
        , verbose_name="Внешний ключ к столбцу"
        , db_comment='{"name":"Внешний ключ к столбцу",}'
        , help_text="Внешний ключ к столбцу",
    )
    oid = models.IntegerField(null=True, blank=True)  # Дополнительный идентификатор
    comment = models.CharField(max_length=255, blank=True, null=True)  # Комментарий к столбцу
    type = models.CharField(max_length=255, blank=True, null=True)  # Тип данных
    default = models.CharField(max_length=255, blank=True, null=True)  # Значение по умолчанию
    expression = models.CharField(max_length=255, blank=True, null=True)  # Выражение для генерации
    is_nullable = models.BooleanField(null=True, blank=True)  # Может ли быть NULL
    is_generated = models.BooleanField(null=True, blank=True)  # Сгенерированный столбец
    is_check = models.BooleanField(null=True, blank=True)  # Проверка
    is_unique = models.BooleanField(null=True, blank=True)  # Уникальность
    is_primary_key = models.BooleanField(null=True, blank=True)  # Первичный ключ
    is_excluded = models.BooleanField(null=True, blank=True)  # Исключение

    class Meta:
        db_table = 'data_value'
        unique_together = [['data_table', 'name', ]]
        ordering = ['-created_at']  # Сортировка по дате создания (по убыванию)
        verbose_name = '04 Значения таблицы'  # Указываем имя таблицы в админке
        verbose_name_plural = '04 Значения таблицы'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.data_table} - {self.type} - {self.name}' or 'NO DATA'


# =============================================== Группировки источников ===============================================
class DataAssetGroup(SystemColumns):
    """
    Названия групп источников данных.
    Ограничение уникальность:
     - Названия групп источников данных.
    """

    name = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Названия групп источников данных."
        , help_text="Названия групп источников данных.",
    )
    description = models.TextField(
        blank=True, null=True
        , verbose_name="Описание групп источников данных."
        , help_text="Описание групп источников данных.",
    )

    class Meta:
        db_table = 'data_asset_group'  # Указываем имя таблицы в базе данных
        unique_together = [["name", ]]
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.name}' or 'NO DATA'


class DataAssetGroupAsset(SystemColumns):
    """
    Связь между. DataAssetGroup и DataAsset.
    Наложение ограничений:
     - Группировка источников данных;
     - Список описанных источников данных.
    """

    name = models.ForeignKey(
        'DataAssetGroup', on_delete=models.CASCADE
        , related_name='related_group'
        , verbose_name="Названия групп источников данных."
        , help_text="Названия групп источников данных."
    )
    data_assets = models.ForeignKey(
        'DataAsset', on_delete=models.CASCADE
        , related_name='related_assets'
        , verbose_name="Список описанных источников данных."
        , help_text="Список описанных источников данных."
    )

    class Meta:
        db_table = 'data_asset_group_list'
        unique_together = [["name", "data_assets", ]]
        verbose_name = '__ Группа источников'
        verbose_name_plural = '__ Группы источников'

    def __str__(self):
        return f'{self.name} - {self.data_assets}' or 'NO DATA'


class DataModelGroup(SystemColumns):
    """
    Названия групп моделей данных.
    Ограничение на уникальность:
     - Названия групп источников данных;
     - Группировка источников данных.
     """

    name = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Названия групп источников данных."
        , help_text="Названия групп источников данных.",
    )
    data_models = models.ManyToManyField(
        'DataModel'
        , related_name='f_model'
        , verbose_name="Группировка источников данных."
        , help_text="Группировка источников данны."
    )

    class Meta:
        db_table = 'data_model_group'  # Указываем имя таблицы в базе данных
        # unique_together = [['name', 'data_models', ]] # накладываем ограничение на уникальность
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.name} - {self.data_models}' or 'NO DATA'


class DataTableGroup(SystemColumns):
    """
    Названия групп таблиц данных.
    Ограничение на уникальность:
     - Названия групп источников данных;
     - Группировка источников данных.
    """

    name = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Названия групп источников данных."
        , help_text="Названия групп источников данных.",
    )
    data_tables = models.ManyToManyField(
        'DataTable'
        , related_name='f_table'
        , verbose_name="Группировка источников данных."
        , help_text="Группировка источников данны."
    )

    class Meta:
        db_table = 'data_table_group'  # Указываем имя таблицы в базе данных
        # unique_together = [['group', 'data_table',]]  # накладываем ограничение на уникальность
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.name} - {self.data_tables}' or 'NO DATA'


class DataValueGroup(SystemColumns):
    """
    Названия групп столбцов данных.
    Ограничение на уникальность:
     - Названия групп столбцов данных;
     - Группировка источников данных.
    """

    name = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Названия групп столбцов данных."
        , help_text="Названия групп столбцов данных.",
    )
    data_values = models.ManyToManyField(
        'DataValue'
        , related_name='f_value'
        , verbose_name="Группировка источников данных."
        , help_text="Группировка источников данны."
    )

    class Meta:
        db_table = 'data_value_groups'  # Указываем имя таблицы в базе данных
        # unique_together = [['name', 'data_values',]]  # накладываем ограничение на уникальность
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке

    def __str__(self):
        return f'{self.name} - {self.data_values}' or 'NO DATA'
