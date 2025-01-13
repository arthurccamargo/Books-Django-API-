# Generated by Django 5.1.3 on 2025-01-13 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0003_remove_book_book_id_book_id_alter_book_book_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_authors',
            field=models.CharField(default='', help_text='Nome do autor do livro', max_length=150),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_description',
            field=models.TextField(default='', help_text='Descrição do livro'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_selfLink',
            field=models.CharField(default='', help_text='Link do livro', max_length=100),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_title',
            field=models.CharField(default='', help_text='Título do livro', max_length=100),
        ),
    ]
