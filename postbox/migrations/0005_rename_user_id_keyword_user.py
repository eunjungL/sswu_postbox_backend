# Generated by Django 3.2.5 on 2021-07-14 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postbox', '0004_alter_keyword_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyword',
            old_name='user_id',
            new_name='user',
        ),
    ]