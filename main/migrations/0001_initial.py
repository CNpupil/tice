# Generated by Django 3.2.8 on 2023-03-25 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(db_index=True, default='null', max_length=50, unique=True)),
                ('expire_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(db_index=True, default='null', max_length=50, unique=True)),
                ('name', models.CharField(default='null', max_length=50)),
                ('password', models.CharField(default='null', max_length=50)),
                ('email', models.CharField(db_index=True, default='null', max_length=50, unique=True)),
                ('token', models.CharField(default='null', max_length=50)),
                ('auth', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
