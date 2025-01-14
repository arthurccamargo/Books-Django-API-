# Generated by Django 5.1.3 on 2025-01-14 04:03

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_rest', '0005_alter_book_book_selflink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='average_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='book',
            name='rating_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('book_title', 'book_authors'), name='unique_book_title_author'),
        ),
        migrations.AddField(
            model_name='rating',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='api_rest.book'),
        ),
    ]