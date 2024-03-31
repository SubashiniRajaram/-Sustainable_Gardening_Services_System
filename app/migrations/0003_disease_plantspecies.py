# Generated by Django 5.0.1 on 2024-03-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_fertilizer_item_tip'),
    ]

    operations = [
        migrations.CreateModel(
            name='disease',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('common_name', models.CharField(max_length=255, null=True)),
                ('other_name', models.CharField(max_length=255, null=True)),
                ('scientific_name', models.CharField(max_length=255, null=True)),
                ('family', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(max_length=255, null=True)),
                ('solution', models.TextField(max_length=255, null=True)),
                ('host', models.CharField(max_length=255, null=True)),
                ('image', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='PlantSpecies',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('common_name', models.CharField(max_length=255)),
                ('scientific_name', models.CharField(max_length=255)),
                ('other_name', models.CharField(blank=True, max_length=255)),
                ('cycle', models.CharField(max_length=255)),
                ('watering', models.CharField(max_length=255)),
                ('sunlight', models.CharField(max_length=255)),
                ('default_image_original_url', models.URLField()),
                ('default_image_thumbnail', models.URLField()),
            ],
        ),
    ]
