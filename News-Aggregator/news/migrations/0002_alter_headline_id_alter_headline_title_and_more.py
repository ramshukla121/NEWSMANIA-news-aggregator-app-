# Generated by Django 4.2.20 on 2025-05-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headline',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='headline',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='headline',
            name='url',
            field=models.URLField(),
        ),
    ]
