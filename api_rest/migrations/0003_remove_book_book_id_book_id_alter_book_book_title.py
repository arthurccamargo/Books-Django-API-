# Generated by Django 5.1.3 on 2024-12-13 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0002_alter_book_book_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_id',
        ),
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='book_title',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
