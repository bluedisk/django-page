# Generated by Django 2.1.7 on 2020-01-01 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0014_auto_20200101_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='special',
            new_name='page_type',
        ),
    ]
