# Generated by Django 3.2.6 on 2021-08-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_app', '0003_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='english',
            name='english',
            field=models.TextField(default='placeholder'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='korean',
            name='foreign_phrase',
            field=models.TextField(default='placeholder'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='korean',
            name='notes',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
