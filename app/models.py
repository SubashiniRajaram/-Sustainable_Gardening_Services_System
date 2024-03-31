from django.db import models

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
      return self.name
    
from embed_video.fields import EmbedVideoField

class Item(models.Model):
    video = EmbedVideoField()
    description=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=255,null=True)
    def __str__(self):
      return self.type


class Fertilizer(models.Model):
    video = EmbedVideoField()
    description=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=255,null=True)
    def __str__(self):
      return self.type

class tip(models.Model):
    video = EmbedVideoField()
    description=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=255,null=True)
    def __str__(self):
      return self.type
      
class PlantSpecies(models.Model):
    id = models.IntegerField(primary_key=True)
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    other_name = models.CharField(max_length=255, blank=True)
    cycle = models.CharField(max_length=255)
    watering = models.CharField(max_length=255)
    sunlight = models.CharField(max_length=255)
    default_image_original_url = models.URLField()
    default_image_thumbnail = models.URLField()
    def __str__(self) -> str:
        return self.common_name

class disease(models.Model):
    id = models.IntegerField(primary_key=True)
    common_name=models.CharField(max_length=255,null=True)
    other_name=models.CharField(max_length=255,null=True)
    scientific_name = models.CharField(max_length=255,null=True)
    family=models.CharField(max_length=255,null=True)
    description=models.TextField(max_length=255,null=True)
    solution=models.TextField(max_length=255,null=True)
    host=models.CharField(max_length=255,null=True)
    image = models.URLField()


    def __str__(self) -> str:
        return self.common_name
class Plant(models.Model):
    id = models.IntegerField(primary_key=True)
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    cycle = models.CharField(max_length=255)
    watering = models.CharField(max_length=255)
    indoor=models.BooleanField(max_length=255,null=True)
    # watering_general_benchmark_value = models.CharField(max_length=255)
    # watering_general_benchmark_unit = models.CharField(max_length=255)
    sunlight = models.CharField(max_length=255)
    maintenance = models.CharField(max_length=255)
    carelevel=models.CharField(max_length=255, null=True)
    description=models.TextField()
    flowering=models.BooleanField(max_length=255,null=True)
    pets=models.BooleanField(max_length=255,null=True)
    fruits=models.BooleanField(max_length=255,null=True)
    image = models.URLField(null=True)


    def __str__(self) -> str:
        return self.common_name
