# Generated by Django 5.0.3 on 2024-05-07 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_remove_book_isbn_book_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='Book',
        ),
        migrations.RemoveField(
            model_name='review',
            name='Reader',
        ),
        migrations.DeleteModel(
            name='Loan',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
