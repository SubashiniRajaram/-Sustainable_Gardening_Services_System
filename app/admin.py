from django.contrib import admin
from .models import Product
# Register your models here.
from embed_video.admin import AdminVideoMixin
from .models import Item,disease,PlantSpecies
from .models import Fertilizer,tip,Plant

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass
class PlantSpeciesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PlantSpecies._meta.fields]
class DiseasesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in disease._meta.fields]
class PlantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Plant._meta.fields]
    
admin.site.register(Item, MyModelAdmin)
admin.site.register(Fertilizer,MyModelAdmin)
admin.site.register(tip,MyModelAdmin)
admin.site.register(Product)
admin.site.register(PlantSpecies,PlantSpeciesAdmin)
admin.site.register(disease,DiseasesAdmin)
admin.site.register(Plant, PlantAdmin)
