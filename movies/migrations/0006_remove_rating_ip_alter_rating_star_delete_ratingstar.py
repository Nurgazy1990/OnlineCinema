# Generated by Django 4.0 on 2022-01-17 19:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='ip',
        ),
        migrations.AlterField(
            model_name='rating',
            name='star',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.DeleteModel(
            name='RatingStar',
        ),
    ]
