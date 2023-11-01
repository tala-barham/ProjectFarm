from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Farm(models.Model):
    name = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=1)
    location=models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    
class Farmer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Resource(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    farm_resource=models.ManyToManyField(Farm)

    def __str__(self):
        return str(self.quantity)
    
class AnimalType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Animal(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    health_status = models.CharField(max_length=100)
    resources = models.ManyToManyField(Resource)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE) 

    def __str__(self):
        return self.gender






