# Generated by Django 4.0 on 2022-01-17 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_user_spam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='spam',
        ),
    ]
