# Generated by Django 5.0.7 on 2025-02-14 22:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_data_asset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataassetgroupasset',
            name='data_assets',
            field=models.ForeignKey(help_text='Список описанных источников данных.', on_delete=django.db.models.deletion.CASCADE, related_name='related_assets', to='my_data_asset.dataasset', verbose_name='Список описанных источников данных.'),
        ),
        migrations.AlterField(
            model_name='dataassetgroupasset',
            name='name',
            field=models.ForeignKey(help_text='Названия групп источников данных.', on_delete=django.db.models.deletion.CASCADE, related_name='related_group', to='my_data_asset.dataassetgroup', verbose_name='Названия групп источников данных.'),
        ),
        migrations.AlterField(
            model_name='datavalue',
            name='data_table',
            field=models.ForeignKey(blank=True, db_comment='{"name":"Список таблиц данных моделей.",}', help_text='Список таблиц данных моделей.', null=True, on_delete=django.db.models.deletion.CASCADE, to='my_data_asset.datatable', verbose_name='Список таблиц данных моделей.'),
        ),
        migrations.AlterField(
            model_name='datavalue',
            name='name',
            field=models.CharField(blank=True, db_comment='{"name":"Название",}', help_text='Название', max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='datavalue',
            name='parent',
            field=models.ForeignKey(blank=True, db_comment='{"name":"Внешний ключ к столбцу",}', help_text='Внешний ключ к столбцу', null=True, on_delete=django.db.models.deletion.CASCADE, to='my_data_asset.datavalue', verbose_name='Внешний ключ к столбцу'),
        ),
        migrations.AlterUniqueTogether(
            name='dataasset',
            unique_together={('url',)},
        ),
        migrations.AlterUniqueTogether(
            name='dataassetgroup',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='dataassetstatus',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='dataassettype',
            unique_together={('name',)},
        ),
        migrations.AlterUniqueTogether(
            name='datamodel',
            unique_together={('data_asset', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='datatable',
            unique_together={('data_model', 'type', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='datavalue',
            unique_together={('data_table', 'name')},
        ),
    ]
