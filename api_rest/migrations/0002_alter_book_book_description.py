# Generated by Django 5.1.3 on 2024-12-01 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_description',
            field=models.TextField(default=''),
        ),
    ]
