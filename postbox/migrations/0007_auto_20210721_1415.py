# Generated by Django 3.1.6 on 2021-07-21 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postbox', '0006_alter_keyword_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notice',
            name='store',
            field=models.BooleanField(default=False),
        ),
    ]
