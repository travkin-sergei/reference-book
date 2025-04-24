from django.db import models
from django.db.models.functions import Now

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
        db_table = f'{db_schema}\".\"asset_type'  # Указываем имя таблицы в базе данных
        ordering = ['name']  # Сортировка по дате создания (по убыванию)
        unique_together = (('name',),)
        verbose_name = '010 Тип'  # Указываем имя таблицы в админке
        verbose_name_plural = '010 Типы'  # Указываем имя таблицы в админке


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
    res_url = models.URLField(
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
        verbose_name = '020 Домен'  # Указываем имя таблицы в админке
        verbose_name_plural = '020 Домены'  # Указываем имя таблицы в админке


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
        verbose_name = '030 Детализация'  # Указываем имя таблицы в админке
        verbose_name_plural = '030 Детализация'  # Указываем имя таблицы в админке


class Asset(BaseModel):
    """Статистка источника данных."""

    type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    domain = models.ForeignKey(AssetDomain, on_delete=models.CASCADE)
    details = models.ForeignKey(AssetDetails, on_delete=models.CASCADE)
    version = models.CharField(
        max_length=255
        , verbose_name="Версия данных."
        , db_comment='{"name":"Версия данных.",}'
        , help_text="Версия данных.",
    )
    description = models.CharField(
        blank=True, null=True
        , max_length=255
        , verbose_name="Описание."
        , db_comment='{"name":"Описание.",}'
        , help_text="Описание",
    )
    res_url = models.URLField(
        blank=True, null=True
        , verbose_name="Ссылка на ресурс."
        , db_comment='{"name":"Ссылка на ресурс.",}'
        , help_text="Ссылка на ресурс",
    )
    docs_url = models.URLField(
        blank=True, null=True
        , verbose_name="Нормативная документация."
        , db_comment='{"name":"Нормативная документация.",}'
        , help_text="Нормативная документация.",
    )
    last_update = models.DateTimeField(blank=True, null=True)
    total_row = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.type}-{self.domain}-{self.details}-{self.version}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"assets'  # Указываем имя таблицы в базе данных
        ordering = ['type', 'domain', 'details', 'version', ]  # Сортировка по дате создания (по убыванию)
        unique_together = (('type', 'domain', 'details', 'version'),)
        verbose_name = '040 Источник'  # Указываем имя таблицы в админке
        verbose_name_plural = '040 Источники'  # Указываем имя таблицы в админке


class AssetColumn(BaseModel):
    """Описание столбца в таблице источника данных."""

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(
        max_length=255,
        verbose_name="Имя столбца",
        help_text="Имя столбца в таблице.",
    )
    data_type = models.CharField(
        max_length=128,
        verbose_name="Тип данных",
        help_text="Тип данных в этом столбце.",
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name="Описание",
        help_text="Описание назначения или значений столбца.",
    )
    is_nullable = models.BooleanField(
        default=True,
        verbose_name="Допускает NULL?",
        help_text="Может ли это поле содержать NULL."
    )

    def __str__(self):
        return f'{self.asset}={self.name}'

    class Meta:
        db_table = f'{db_schema}\".\"asset_columns'
        verbose_name = '050 Столбец'
        verbose_name_plural = '050 Столбцы'
        ordering = ['asset', 'name']
        unique_together = (('asset', 'name'),)


class AssetCategory(BaseModel):
    """Категория, создаваемая пользователем, для группировки источников данных."""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название категории",
        help_text="Название категории, заданное пользователем.",
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name="Описание",
        help_text="Дополнительное описание категории."
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = f'{db_schema}\".\"asset_category'
        verbose_name = '100 Категория'
        verbose_name_plural = '100 Категории'
        ordering = ['name']


class AssetCategoryRelation(BaseModel):
    """Связь между источниками и пользовательскими категориями."""

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = f'{db_schema}\".\"asset_category_relation'
        verbose_name = '110 Связь категория-источник'
        verbose_name_plural = '110 Связи категория-источник'
        unique_together = (('asset', 'category'),)
