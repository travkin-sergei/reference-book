from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet

from .models import (
    Language, generate_unique_code,
    Synonym,
    Object,
    ObjectMap,
    ObjectMapSub,
    ObjectCodeType,
    ObjectCode,
    ObjectMapType, ObjectCodeSub, Info,
)


class BaseAdmin(admin.ModelAdmin):
    """Базовые настройки."""
    readonly_fields = 'user', 'created_at', 'updated_at',
    exclude = 'user',

    def save_model(self, request, obj, form, change):
        """Сохранение автора записи."""
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        # Если объект уже существует, делаем поля readonly
        if obj:
            return self.readonly_fields
        return self.readonly_fields



@admin.register(Language)
class LanguageAdmin(BaseAdmin):
    """Админка для списка языков."""

    list_display = 'language', 'name',
    search_fields = 'language', 'name',


@admin.register(Synonym)
class SynonymAdmin(BaseAdmin):
    """Список названий."""

    list_display = 'name', 'language',
    search_fields = 'name', 'language__language',
    autocomplete_fields = 'language',


@admin.register(ObjectMapType)
class ObjectMapTypeAdmin(BaseAdmin):
    list_display = 'map_type',
    list_display_links = 'map_type',
    search_fields = 'map_type',


class InfoForm(forms.ModelForm):
    """Кастомная форма для GeoInfo, чтобы сделать поле user необязательным в форме."""

    class Meta:
        model = Info
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'user' in self.fields:
            self.fields['user'].required = False  # Делаем поле user необязательным в форме


class InfoFormSet(BaseInlineFormSet):
    def save_new(self, form, commit=True):
        """Переопределяем метод для установки автора при создании новой записи."""
        instance = super().save_new(form, commit=False)
        instance.user = self.request.user  # Устанавливаем автора
        instance.task = self.instance.task  # Устанавливаем task из родительского Object
        if commit:
            instance.save()
        return instance

    def save_existing(self, form, instance, commit=True):
        """Переопределяем метод для установки автора и task при изменении существующей записи."""
        instance = super().save_existing(form, instance, commit=False)
        instance.user = self.request.user  # Устанавливаем автора
        instance.task = self.instance.task  # Устанавливаем task из родительского Object
        if commit:
            instance.save()
        return instance


class InfoInline(admin.TabularInline):
    """Inline для редактирования дополнительной информации о геообъекте."""

    model = Info
    extra = 1
    form = InfoForm  # Используем кастомную форму
    formset = InfoFormSet
    exclude = ('user', 'task')  # Скрываем поля user и task из формы

    def get_formset(self, request, *args, **kwargs):
        """Переопределяем метод, чтобы передать request в FormSet."""
        formset = super().get_formset(request, *args, **kwargs)
        formset.request = request  # Передаем request в FormSet
        return formset


@admin.register(Object)
class ObjectAdmin(BaseAdmin):
    """Админка для списка уникальных геообъектов."""

    inlines = [InfoInline]

    readonly_fields = 'geo_id', 'user',
    list_display = 'geo_id', 'is_active', 'object_name', 'user', 'task',
    list_display_links = 'geo_id', 'object_name', 'user', 'task',
    search_fields = 'geo_id', 'object_name', 'task',

    autocomplete_fields = ['name']
    filter_horizontal = ['name']

    def get_queryset(self, request):
        """Отображение связанных в модели многие ко многим."""
        result = Object.objects.prefetch_related("name").all()
        return result

    def save_model(self, request, obj, form, change):
        """Сохранение автора записи и генерация уникального кода."""
        obj.user = request.user
        if not obj.object_code:  # Проверяем, что код еще не задан
            obj.object_code = generate_unique_code()  # Генерируем уникальный код
            # Проверяем уникальность кода
            existing_codes = set(Object.objects.filter(is_active=True).values_list('geo_id', flat=True))
            while obj.object_code in existing_codes:
                obj.object_code = generate_unique_code()
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Сохранение автора и task для каждой записи в форме."""
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.user_id:  # Устанавливаем автора, если он еще не задан
                instance.user = request.user
            if not instance.task:  # Устанавливаем task, если он еще не задан
                instance.task = form.instance.task  # Берем task из родительского Object
            instance.save()
        formset.save_m2m()


@admin.register(ObjectCodeType)
class ObjectCodeTypeAdmin(BaseAdmin):
    list_display = 'id', 'code_type',
    list_display_links = 'id',
    search_fields = 'code_type',


class ObjectCodeSubInline(admin.TabularInline):
    """Инлайн для управления связями между ObjectCode и Object с дополнительным полем code_name."""

    model = ObjectCodeSub
    extra = 1
    autocomplete_fields = 'object', 'name',
    exclude = 'user',


# 03.01 Справочник
@admin.register(ObjectCode)
class ObjectCodeAdmin(BaseAdmin):
    """Админка для ObjectCode."""

    inlines = [ObjectCodeSubInline]

    list_display = 'geo', 'code_type',
    list_display_links = 'geo',
    search_fields = 'geo__object_name', 'code_type__code_type',
    autocomplete_fields = 'geo', 'code_type',

    def save_formset(self, request, form, formset, change):
        """Автоматическое заполнение поля user в инлайнах."""
        instances = formset.save(commit=False)
        for instance in instances:
            # Убедитесь, что поле user не используется, если его нет в модели
            instance.save()
        formset.save_m2m()  # Сохраняем связи many-to-many, если они есть


class ObjectMapInline(admin.TabularInline):
    """Инлайн для управления связями между ObjectCode и Object с дополнительным полем code_name."""

    model = ObjectMapSub
    extra = 1
    autocomplete_fields = 'object',


@admin.register(ObjectMap)
class ObjectMapAdmin(BaseAdmin):
    """Админка для ObjectMap."""

    inlines = [ObjectMapInline]

    list_display = 'geo',
    list_display_links = 'geo',
    search_fields = 'geo__object_name', 'sub_objects__code_type__map_type',
    autocomplete_fields = 'geo',

    def get_search_results(self, request, queryset, search_term):
        """Фильтруем результаты поиска для поля geo."""
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Фильтруем только те объекты, у которых is_active = True
        queryset = queryset.filter(geo__is_active=True)

        return queryset, use_distinct
