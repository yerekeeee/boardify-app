# Generated by Django 5.1.2 on 2024-10-29 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0002_alter_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='price',
            field=models.IntegerField(default='', verbose_name='Цена'),
        ),
    ]