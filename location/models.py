from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   null=True)
    
    def __str__(self) -> str:
        return self.name