# Generated by Django 4.0 on 2022-01-18 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_favorites_user_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='age',
            field=models.PositiveSmallIntegerField(verbose_name='Возраст'),
        ),
    ]
