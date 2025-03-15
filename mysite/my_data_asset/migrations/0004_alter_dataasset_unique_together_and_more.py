# Generated by Django 5.0.7 on 2025-02-16 15:13


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_data_asset', '0003_alter_dataasset_options_alter_datavalue_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dataasset',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='dataasset',
            name='comment',
            field=models.TextField(blank=True, db_comment='{"name":"Описание ресурса",}', help_text='Описание ресурса.', null=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='dataasset',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='dataassetgroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='dataassetgroupasset',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='dataassetstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='dataassettype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='comment',
            field=models.TextField(blank=True, help_text='Комментарий.', null=True),
        ),
        migrations.AlterField(
            model_name='datamodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='datamodelgroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='datatable',
            name='comment',
            field=models.TextField(blank=True, help_text='Комментарий.', null=True),
        ),
        migrations.AlterField(
            model_name='datatable',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='datatablegroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='datavalue',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AlterField(
            model_name='datavaluegroup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_comment='{"name":"Строка в базе данных обновлена.",}', help_text='Дата обновления строки в текущей базе данных.'),
        ),
        migrations.AddConstraint(
            model_name='dataasset',
            constraint=models.UniqueConstraint(fields=('url',), name='unique_data_asset_url'),
        ),
    ]
