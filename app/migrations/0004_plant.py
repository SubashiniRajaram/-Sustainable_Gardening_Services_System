# Generated by Django 5.0.1 on 2024-03-18 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_disease_plantspecies'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('common_name', models.CharField(max_length=255)),
                ('scientific_name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('cycle', models.CharField(max_length=255)),
                ('watering', models.CharField(max_length=255)),
                ('indoor', models.BooleanField(max_length=255, null=True)),
                ('sunlight', models.CharField(max_length=255)),
                ('maintenance', models.CharField(max_length=255)),
                ('carelevel', models.CharField(max_length=255, null=True)),
                ('description', models.TextField()),
                ('flowering', models.BooleanField(max_length=255, null=True)),
                ('pets', models.BooleanField(max_length=255, null=True)),
                ('fruits', models.BooleanField(max_length=255, null=True)),
                ('image', models.URLField(null=True)),
            ],
        ),
    ]
