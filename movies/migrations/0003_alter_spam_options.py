# Generated by Django 4.0 on 2022-01-17 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_spam'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spam',
            options={'verbose_name': 'Спам', 'verbose_name_plural': 'Спамы'},
        ),
    ]