import random
import string

from simple_history.models import HistoricalRecords

from django.contrib.auth.models import User
from django.db import models
from django.db.models import DateField

db_schema = 'my_geo_id'


def generate_unique_code(length=6):
    """Генерация набора из чисел и букв в нижнем регистре, с запретом на полностью числовые значения."""

    characters = string.ascii_lowercase + string.digits
    while True:
        # Генерируем случайный код заданной длины
        code = ''.join(random.choice(characters) for _ in range(length))
        # Проверяем, содержит ли код хотя бы одну букву
        if any(c.isalpha() for c in code):
            return code


class BaseModel(models.Model):
    """Базовый класс модели. Сюда вынесены все системные поля."""

    creation_at = models.DateTimeField(
        auto_now_add=True
        , verbose_name='Создано'
        , help_text="Создано"

    )
    update_at = models.DateTimeField(
        auto_now=True
        , verbose_name='Обновлено'
        , help_text="Обновлено"

    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
        , verbose_name='Автор'
        , help_text="Автор"
    )
    is_active = models.BooleanField(
        default=True
        , verbose_name='Запись активна?'
        , help_text="Запись активна?"
    )
    task = models.URLField(
        verbose_name='Задача в Jira'
        , help_text="Задача в Jira"

    )

    class Meta:
        abstract = True


class Language(BaseModel):
    """Список используемых языков в модели данных."""

    language = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=255)
    history = HistoricalRecords(table_name='geo_language_history')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_language'
        db_table_comment = '{"name":"Список языков","description":"список языков"}'
        verbose_name = '01 список языков'
        verbose_name_plural = '01 список языков'


class GeoNames(BaseModel):
    """"Варианты названий геообъектов."""

    name = models.CharField(
        primary_key=True, max_length=255
        , verbose_name='наименование'
        , help_text="наименование"
    )
    language = models.ForeignKey(
        'Language',
        related_name='names', on_delete=models.CASCADE
        , verbose_name='язык'
        , help_text="язык"
    )
    date_start = DateField(
        null=True, blank=True
        , verbose_name='Дата начала действия'
        , help_text="Дата начала действия"

    )
    date_stop = DateField(
        null=True, blank=True
        , verbose_name='Дата прекращения действия'
        , help_text="Дата прекращения действия"

    )
    history = HistoricalRecords(table_name='geo_names_history')

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_names'
        db_table_comment = (
            '{'
            '"name":"Название геобъекта",'
            '"description":"Таблица создана для ведения списка уникальных геообъектов",'
            '}'
        )
        verbose_name = '01.01 название геобъекта'
        verbose_name_plural = '01.01 названия геобъектов'

    def __str__(self):
        return f'{self.language}-{self.name}'


class GeoObject(BaseModel):
    """
    Список гео объектов с уникальными кодами
    Важно!!! иметь только один геобъект даже если у него разные названия
    """

    object_code = models.CharField(
        primary_key=True, max_length=6
        , verbose_name='уникальный код гео объекта'
        , help_text="кода автогенерируемый в модели"
    )
    object_name = models.CharField(
        unique=True, max_length=255
        , verbose_name='техническое наименование'
        , help_text="подтягивается из языковой модели"

    )
    geo_name = models.ManyToManyField(
        'GeoNames'
        , related_name='geo_objects'
        , verbose_name="Все варианты названий"
        , help_text="Все варианты названий"
    )
    date_start = DateField(
        null=True, blank=True
        , verbose_name='Дата начала действия',
    )
    date_stop = DateField(
        null=True, blank=True
        , verbose_name='дата прекращения действия',
    )

    history = HistoricalRecords(table_name='geo_object_history')

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object'
        db_table_comment = '{"name":"Геообъекты","description":"Таблица создана для ведения списка уникальных геообъектов"}'
        verbose_name = '02 Геообъект'
        verbose_name_plural = '02 Геообъекты'

    def __str__(self):
        return f'{self.object_code}-{self.object_name}'

    def save(self, *args, **kwargs):
        # Генерируем уникальный код, если он не задан и объект новый
        if not self.object_code and not self.pk:  # Проверяем, что объект новый
            unique_code = generate_unique_code().lower()  # Генерируем уникальный код в нижнем регистре
            # Проверяем уникальность кода среди активных объектов
            existing_codes = set(GeoObject.objects.filter(is_active=True).values_list('object_code', flat=True))
            while unique_code in existing_codes:
                unique_code = generate_unique_code().lower()  # Генерируем новый код в нижнем регистре
            self.object_code = unique_code
        super().save(*args, **kwargs)


class GeoObjectMapType(BaseModel):
    """Тип в группе объектов"""

    map_type = models.CharField(
        max_length=255
        , verbose_name='Тип группировки'
        , help_text="Тип группировки"
    )
    history = HistoricalRecords(table_name='geo_object_map_type_history')

    def __str__(self):
        return f'{self.map_type}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_map_type'
        db_table_comment = '{"name":"тип связи гео объекта","description":""}'
        verbose_name = '04 тип связи гео'
        verbose_name_plural = '04 тип связи гео'


class GeoObjectSynonym(BaseModel):
    """Все варианты географических названий."""

    geo = models.ForeignKey(
        'GeoObject', on_delete=models.CASCADE
        , help_text="Ссылка на объект"
    )
    language = models.ForeignKey(
        'Language', on_delete=models.CASCADE
        , help_text="alfa-2 языка"
    )
    name = models.CharField(
        max_length=255
        , help_text="Текст"
    )

    def __str__(self):
        return f'{self.language}-{self.name}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_synonym'
        db_table_comment = '{"name":"Синонимы названий геообъектов",}'
        verbose_name = '00 Синонимы геообъекта'
        verbose_name_plural = '02 Синонимы геообъектов'
        unique_together = 'geo', 'language', 'name',


class GeoObjectCodeType(BaseModel):
    """Типы кодификации."""

    code_type = models.CharField(max_length=255, )
    history = HistoricalRecords(table_name='geo_object_code_type_history')

    def __str__(self):
        return f'{self.code_type}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_code_type'
        verbose_name = '03 Тип кодов'
        verbose_name_plural = '03 Типы кодов'


class GeoObjectCode(BaseModel):
    """Варианты кодов геообъектов."""

    main = models.ForeignKey('GeoObject', on_delete=models.CASCADE)
    code_type = models.ForeignKey(GeoObjectCodeType, on_delete=models.CASCADE)
    history = HistoricalRecords(table_name='geo_object_code_history')

    def __str__(self):
        return f'{self.main} - {self.code_type}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_code'
        ordering = ['main','-code_type']
        verbose_name = '03.01 Справочник'
        verbose_name_plural = '03.01 Справочники'


class GeoObjectCodeSub(models.Model):
    """Промежуточная модель для связи GeoObjectCode и GeoObject с дополнительным полем code_name."""

    geo_object_code = models.ForeignKey(GeoObjectCode, on_delete=models.CASCADE, related_name='sub_objects')
    geo_object = models.ForeignKey(GeoObject, on_delete=models.CASCADE)
    name = models.ForeignKey(GeoNames, null=True, blank=True, on_delete=models.CASCADE)
    code_name = models.CharField(max_length=255)
    is_group = models.BooleanField(
        default=False
        , db_comment='{'
                     '"name":"это группа объектов текущегосправочника?."'
                     '"description":"это группа объектов текущегосправочника?"'
                     '}'
        , verbose_name='это группа объектов текущегосправочника?'
        , help_text='это группа объектов текущегосправочника?'
    )
    history = HistoricalRecords(table_name='geo_object_code_sub_history')

    def __str__(self):
        return f'{self.geo_object_code} - {self.geo_object} ({self.code_name})'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_code_sub'
        db_table_comment = '{"name":"geo_object_code_sub",}'
        verbose_name = '03.02 Справочник'
        verbose_name_plural = '03.02 Справочники'
        unique_together = 'geo_object_code', 'geo_object',


class GeoObjectMap(BaseModel):
    """Группировки геообъектов."""

    main = models.ForeignKey('GeoObject', on_delete=models.CASCADE)

    history = HistoricalRecords(table_name='geo_object_map_history')

    def __str__(self):
        return f'{self.main}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_map'
        verbose_name = '04.01 Группировка'
        verbose_name_plural = '04.01 Группировка'


class GeoObjectMapSub(models.Model):
    """Промежуточная модель для связи GeoObjectCode и GeoObject с дополнительным полем code_name."""

    geo_object_code = models.ForeignKey(GeoObjectMap, on_delete=models.CASCADE, related_name='sub_objects')
    geo_object = models.ForeignKey(GeoObject, on_delete=models.CASCADE)
    code_type = models.ForeignKey(GeoObjectMapType, on_delete=models.CASCADE)
    date_start = DateField(
        null=True, blank=True
        , verbose_name='Дата начала действия',
    )
    date_stop = DateField(
        null=True, blank=True
        , verbose_name='дата прекращения действия',
    )
    history = HistoricalRecords(table_name='geo_object_map_sub_history')

    def __str__(self):
        return f'{self.geo_object_code} - {self.geo_object}'

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_object_map_sub'
        db_table_comment = '{"name":"geo_object_map_sub",}'
        verbose_name = '04.02 Группировка'
        verbose_name_plural = '04.02 Группировка'
        # Уникальное ограничение для предотвращения дубликатов
        unique_together = 'geo_object_code', 'geo_object',


class GeoInfo(BaseModel):
    """Дополнительная информация об объекте."""

    geo = models.OneToOneField(
        'GeoObject',
        on_delete=models.CASCADE,
        related_name='geo_info',
        verbose_name='Геообъект'
    )
    area = models.FloatField(
        null=True, blank=True,
        verbose_name='Площадь территории (кв. км)'
    )
    coordinates = models.TextField(
        null=True, blank=True
        , verbose_name='географические координаты.'
    )

    def __str__(self):
        return str({self.geo})

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"geo_info'
        verbose_name = 'Площадь территории'
        verbose_name_plural = 'Площадь территории'


class MapLocation(models.Model):
    """
    Названия
    Координаты
    Картинка
    """

    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='maps/')

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = f'{db_schema}\".\"map_location'
