from django.db import models

# Create your models here.


class Continent(models.Model):
    continentName = models.CharField(primary_key=True, max_length=100)
    continentPopulation = models.BigIntegerField()
    continentArea = models.BigIntegerField()

    class Meta:
        db_table = 'Continent'
        verbose_name = 'Continent Details'


class Country(models.Model):
    continentName = models.ForeignKey(Continent, on_delete=models.CASCADE)
    countryName = models.CharField(primary_key=True, max_length=100)
    countryPopulation = models.BigIntegerField()
    countryArea = models.BigIntegerField()
    countryHospitals = models.BigIntegerField(null=True, blank=True)
    countryParks = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Country'
        verbose_name = 'Country Details'

class City(models.Model):
    countryName = models.ForeignKey(Country,to_field='countryName', on_delete=models.CASCADE)
    cityName = models.CharField(primary_key=True, max_length=100)
    cityPopulation = models.BigIntegerField()
    cityArea = models.BigIntegerField()
    cityRoads = models.BigIntegerField(null=True, blank=True)
    cityTrees = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'City'
        verbose_name = 'City Details'