# Generated by Django 5.0.3 on 2024-05-05 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_date_create_alter_book_date_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='ISBN',
        ),
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
