from django.db import models
from django.db.models.functions import Now
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator

db_schema = 'my_data_asset'


class SystemColumns(models.Model):
    """Набор минимальных системных столбцов."""

    created_at = models.DateTimeField(
        db_default=Now()
        , verbose_name='Создано'
        , help_text="Создано"

    )
    updated_at = models.DateTimeField(
        db_default=Now()
        , verbose_name='Обновлено'
        , help_text="Обновлено"

    )
    is_active = models.BooleanField(
        db_default=True
        , verbose_name='Запись активна?'
        , help_text="Запись активна?"
    )

    class Meta:
        abstract = True


class BaseModel(SystemColumns):
    """Базовая модель приложения Asset."""

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


class AssetType(BaseModel):
    """Типа"""

    name = models.CharField(
        primary_key=True
        , max_length=255
        , verbose_name="Тип данных."
        , db_comment='{"name":"Тип данных.",}'
        , help_text="Тип данных.",
    )
    description = models.CharField(
        blank=True, null=True
        , verbose_name="Описание."
        , db_comment='{"name":"Описание.",}'
        , help_text="Тип данных.",
    )

    def __str__(self):
        return f'{self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"asset_type_2'  # Указываем имя таблицы в базе данных
        ordering = ['name']  # Сортировка по дате создания (по убыванию)
        unique_together = (('name',),)
        verbose_name = '010 AssetType'  # Указываем имя таблицы в админке
        verbose_name_plural = '010 AssetType'  # Указываем имя таблицы в админке


class AssetDomain(BaseModel):
    """Типа"""

    name = models.CharField(
        primary_key=True
        , max_length=255
        , verbose_name="Домен данных."
        , db_comment='{"name":"Домен данных.",}'
        , help_text="Домен данных.",
    )
    description = models.CharField(
        blank=True, null=True
        , verbose_name="Описание."
        , db_comment='{"name":"Описание.",}'
        , help_text="Тип данных.",
    )
    link = models.URLField(
        blank=True, null=True
        , verbose_name="Ссылка на ресурс."
        , db_comment='{"name":"Ссылка на ресурс.",}'
        , help_text="Ссылка на ресурс",
    )

    def __str__(self):
        return f'{self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"asset_domain'  # Указываем имя таблицы в базе данных
        ordering = ['name']  # Сортировка по дате создания (по убыванию)
        unique_together = (('name',),)
        verbose_name = '020 AssetDomain'  # Указываем имя таблицы в админке
        verbose_name_plural = '020 AssetDomain'  # Указываем имя таблицы в админке


class AssetDetails(BaseModel):
    """Типа"""

    name = models.CharField(
        primary_key=True
        , max_length=255
        , verbose_name="Детализация данных."
        , db_comment='{"name":"Детализация данных.",}'
        , help_text="Детализация данных.",
    )
    description = models.CharField(
        blank=True, null=True
        , verbose_name="Описание."
        , db_comment='{"name":"Описание.",}'
        , help_text="Тип данных.",
    )

    def __str__(self):
        return f'{self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"asset_details'  # Указываем имя таблицы в базе данных
        ordering = ['name']  # Сортировка по дате создания (по убыванию)
        unique_together = (('name',),)
        verbose_name = '030 AssetDetails'  # Указываем имя таблицы в админке
        verbose_name_plural = '030 AssetDetails'  # Указываем имя таблицы в админке


class AssetVersion(BaseModel):
    """Типа"""
    name = models.PositiveIntegerField(
        primary_key=True
        , verbose_name="Версия данных."
        , db_comment='{"name":"Версия данных.",}'
        , help_text="Версия данных.",
    )

    def __str__(self):
        return f'{self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"asset_version'  # Указываем имя таблицы в базе данных
        ordering = ['name']  # Сортировка по дате создания (по убыванию)
        unique_together = (('name',),)
        verbose_name = '040 AssetVersion'  # Указываем имя таблицы в админке
        verbose_name_plural = '040 AssetVersion'  # Указываем имя таблицы в админке


class Asset(BaseModel):
    """Статистка источника данных."""

    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    domain = models.ForeignKey(AssetDomain, on_delete=models.CASCADE)
    details = models.ForeignKey(AssetDetails, on_delete=models.CASCADE)
    version = models.ForeignKey(AssetVersion, on_delete=models.CASCADE)
    link = models.URLField(
        blank=True, null=True
        , verbose_name="Ссылка на ресурс."
        , db_comment='{"name":"Ссылка на ресурс.",}'
        , help_text="Ссылка на ресурс",
    )
    description = models.CharField(
        blank=True, null=True
        , max_length=255
        , verbose_name="Описание."
        , db_comment='{"name":"Описание.",}'
        , help_text="Описание",
    )

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"assets_1'  # Указываем имя таблицы в базе данных
        ordering = ['type', 'domain', 'details', 'version', ]  # Сортировка по дате создания (по убыванию)
        unique_together = (('type', 'domain', 'details', 'version'),)
        verbose_name = '050 Asset'  # Указываем имя таблицы в админке
        verbose_name_plural = '050 Asset'  # Указываем имя таблицы в админке


class AssetStat(BaseModel):
    """Статистка источника данных."""

    uir = models.ForeignKey('Asset', on_delete=models.CASCADE)  # Внешний ключ
    period = models.CharField(
        null=True, blank=True
        , verbose_name="Период"
        , db_comment='{"name":"Период",}'
    )
    date_last = models.DateField(
        blank=True, null=True
        , verbose_name="По состоянию на"
        , db_comment='{"name":"По состоянию на",}'
    )
    row_period = models.PositiveIntegerField(
        blank=True, null=True
        , verbose_name="Количество актуализированных строк за период."
        , db_comment='{"name":"Количество актуализированных строк за период.",}'
    )
    version = models.CharField(
        max_length=255, blank=True, null=True
        , verbose_name="Версия"
        , db_comment='{"name":"Версия ресурса.",}'
        , help_text="Версия ресурса.",
    )
    control_1 = models.DecimalField(
        max_digits=10, decimal_places=2
        , blank=True, null=True
        , verbose_name="Контрольная цифра №1."
        , db_comment='{"name":"Контрольная цифра №1.",}'
    )
    control_2 = models.DecimalField(
        max_digits=10, decimal_places=2
        , validators=[MinValueValidator(0)]
        , blank=True, null=True
        , verbose_name="Контрольная цифра №2."
        , db_comment='{"name":"Контрольная цифра №2.",}'
    )

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"assets_stat'  # Указываем имя таблицы в базе данных
        ordering = ['uir', 'date_last']  # Сортировка по дате создания (по убыванию)
        unique_together = (('uir', 'period', 'date_last'),)
        verbose_name = '01.01 Статистика источника данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '01.01 Статистика источника данных'  # Указываем имя таблицы в админке


class DataModel(BaseModel):
    """
    Список описанных моделей источников данных.
    Ограничение уникальность:
     - Список описанных источников данных;
     - Название модели.
    """

    data_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True, blank=True)  # Внешний ключ
    name = models.CharField(max_length=255, blank=True, null=True)  # Схема
    comment = CKEditor5Field(
        help_text="Комментарий.",
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.data_asset} - {self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"models'  # Указываем имя таблицы в базе данных
        unique_together = [["data_asset", "name", ]]
        verbose_name = '2 Модель данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '2 Модели данных'  # Указываем имя таблицы в админке


class DataTable(BaseModel):
    """
    Список таблиц данных моделей.
    Ограничение уникальность:
     - Список таблиц данных моделей;
     - Тип;
     - Название.
    """

    data_model = models.ForeignKey(
        DataModel, on_delete=models.CASCADE, null=True, blank=True
    )  # Внешний ключ
    type = models.CharField(
        max_length=255, blank=True, null=True
    )  # Тип таблицы
    name = models.CharField(
        max_length=255, blank=True, null=True
    )  # Название таблицы данных
    comment = CKEditor5Field(
        blank=True, null=True
        , help_text="Комментарий."
    )

    def __str__(self):
        return f'{self.data_model} - {self.type} - {self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"data_table'  # Указываем имя таблицы в базе данных
        unique_together = [["data_model", "type", "name", ]]
        verbose_name = '3 Таблица данных'  # Указываем имя таблицы в админке
        verbose_name_plural = '3 Таблицы данных'  # Указываем имя таблицы в админке


class DataValue(BaseModel):
    """
    Содержит список полей источников данных.
    Ограничение уникальность:
     - Список таблиц данных моделей;
     - Название.
    """

    data_table = models.ForeignKey(
        DataTable, on_delete=models.CASCADE, null=True, blank=True
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

    def __str__(self):
        return f'{self.data_table} - {self.type} - {self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"value_table'
        unique_together = [['data_table', 'name', ]]
        ordering = ['created_at']  # Сортировка по дате создания (по убыванию)
        verbose_name = '4 Значения таблицы'  # Указываем имя таблицы в админке
        verbose_name_plural = '4 Значения таблицы'  # Указываем имя таблицы в админке


# =============================================== Группировки источников ===============================================
class AssetGroup(SystemColumns):
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

    def __str__(self):
        return f'{self.name}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"asset_group'  # Указываем имя таблицы в базе данных
        unique_together = [["name", ]]
        verbose_name = '060 Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '060 Группы источников'  # Указываем имя таблицы в админке


class DataAssetGroupAsset(SystemColumns):
    """
    Связь между. DataAssetGroup и DataAsset.
    Наложение ограничений:
     - Группировка источников данных;
     - Список описанных источников данных.
    """

    name = models.ForeignKey(
        AssetGroup, on_delete=models.CASCADE
        , related_name='related_group'
        , verbose_name="Названия групп источников данных."
        , help_text="Названия групп источников данных."
    )
    data_assets = models.ForeignKey(
        Asset, on_delete=models.CASCADE
        , related_name='related_assets'
        , verbose_name="Список описанных источников данных."
        , help_text="Список описанных источников данных."
    )

    def __str__(self):
        return f'{self.name} - {self.data_assets}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"asset_group_list'
        unique_together = [["name", "data_assets", ]]
        verbose_name = '__ Группа источников'
        verbose_name_plural = '__ Группы источников'


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
        DataModel
        , related_name='f_model'
        , verbose_name="Группировка источников данных."
        , help_text="Группировка источников данны."
    )

    def __str__(self):
        return f'{self.name} - {self.data_models}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"model_group'  # Указываем имя таблицы в базе данных
        # unique_together = [['name', 'data_models', ]] # накладываем ограничение на уникальность
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке


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
        DataTable
        , related_name='f_table'
        , verbose_name="Группировка источников данных."
        , help_text="Группировка источников данны."
    )

    def __str__(self):
        return f'{self.name} - {self.data_tables}' or 'NO DATA'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"table_group'  # Указываем имя таблицы в базе данных
        # unique_together = [['group', 'data_table',]]  # накладываем ограничение на уникальность
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке


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
        DataValue
        , related_name='f_value'
        , verbose_name="Группировка источников данных."
        , help_text="Группировка источников данны."
    )

    def __str__(self):
        return f'{self.name} - {self.data_values}' or 'NO DATA'

    class Meta:
        db_table = f'{db_schema}\".\"value_groups'  # Указываем имя таблицы в базе данных
        # unique_together = [['name', 'data_values',]]  # накладываем ограничение на уникальность
        verbose_name = '__ Группа источников'  # Указываем имя таблицы в админке
        verbose_name_plural = '__ Группы источников'  # Указываем имя таблицы в админке
