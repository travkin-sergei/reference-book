from django.core.management.base import BaseCommand
from django.core.serializers import deserialize
from ...models import GeoNames
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Импорт данных с upsert и сохранением истории"

    def handle(self, *args, **options):
        self.stdout.write("Импорт данных...")

        # Открываем JSON-файл
        with open("data.json", "r") as f:
            objects = list(deserialize("json", f))

        to_update = []
        to_create = []

        # Получаем существующие записи (GeoNames использует name как primary_key)
        existing_records = {obj.name: obj for obj in GeoNames.objects.all()}

        for obj in objects:
            new_obj = obj.object  # Десериализованный объект

            if new_obj.name in existing_records:
                old_obj = existing_records[new_obj.name]

                # Проверяем изменения (не обновляем user и task)
                fields_to_check = ["language", "date_start", "date_stop"]
                changes = {
                    field:
                        getattr(new_obj, field) for field in fields_to_check if
                    getattr(old_obj, field) != getattr(new_obj, field)
                }

                if changes:
                    to_update.append(new_obj)

                    # Логируем изменения
                    change_log = ", ".join(
                        f"{field}: {getattr(old_obj, field)} -> {getattr(new_obj, field)}" for field in changes)
                    logger.info(f"Обновление {new_obj.name}: {change_log}")

            else:
                to_create.append(new_obj)

        # Массово создаём новые записи
        GeoNames.objects.bulk_create(to_create, ignore_conflicts=True)

        # Массово обновляем существующие записи (django-simple-history сохранит изменения автоматически)
        fields_to_update = ["language", "date_start", "date_stop"]
        GeoNames.objects.bulk_update(to_update, fields_to_update)

        self.stdout.write(
            self.style.SUCCESS(
                f"Импортировано {len(to_create)} новых записей, обновлено {len(to_update)}"
            )
        )
