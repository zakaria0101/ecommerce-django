# Generated by Django 4.1.7 on 2023-05-05 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
    ]
