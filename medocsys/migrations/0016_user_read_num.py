# Generated by Django 3.2.16 on 2023-04-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('medocsys', '0015_auto_20230403_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='read_num',
            field=models.IntegerField(default=1, verbose_name='阅读量'),
        ),
    ]
