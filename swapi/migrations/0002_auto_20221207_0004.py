# Generated by Django 2.2.25 on 2022-12-07 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('alias', models.CharField(blank=True, max_length=150, null=True)),
                ('movie', models.CharField(max_length=150)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FavouritePlanet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('alias', models.CharField(blank=True, max_length=150, null=True)),
                ('planet', models.CharField(max_length=150)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Favourite',
        ),
    ]