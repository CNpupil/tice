# Generated by Django 3.2.8 on 2023-04-24 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20230424_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentinfomation',
            old_name='class_number',
            new_name='class_name',
        ),
    ]
