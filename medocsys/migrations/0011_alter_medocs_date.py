# Generated by Django 3.2.16 on 2023-02-27 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medocsys', '0010_auto_20230226_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medocs',
            name='date',
            field=models.DateField(default='2023-02-27', verbose_name='日期'),
        ),
    ]
