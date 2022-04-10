from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.db.models import Count, Avg, Sum


class ContinentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Continent
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
    
    def validate(self, data):
        continentDetails = Continent.objects.get(continentName = data.get('continentName').continentName)
        continentPopulation = continentDetails.continentPopulation
        continentArea = continentDetails.continentArea
        totalCountryPopulation = Country.objects.filter(continentName = data.get('continentName').continentName).aggregate(Sum('countryPopulation'))
        if totalCountryPopulation['countryPopulation__sum'] == None:
            totalCountryPopulation = data.get('countryPopulation')
        else:
            totalCountryPopulation = totalCountryPopulation['countryPopulation__sum'] + data.get('countryPopulation')
        totalCountryArea = Country.objects.filter(continentName = data.get('continentName').continentName).aggregate(Sum('countryArea'))
        if totalCountryArea['countryArea__sum'] == None:
            totalCountryArea = data.get('countryArea')
        else:
            totalCountryArea = totalCountryArea['countryArea__sum'] + data.get('countryArea')
        if continentPopulation >=  totalCountryPopulation and continentArea >=  totalCountryArea:
            return data
        elif continentPopulation <=  totalCountryPopulation:
            raise serializers.ValidationError('Total of Country population is greater than Contient population')
        elif continentArea <=  totalCountryArea:
            raise serializers.ValidationError('Total of Country area is greater than Contient area')
        else:
            raise serializers.ValidationError('Invalid data')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'

    def validate(self, data):
        countryDetails = Country.objects.get(countryName = data.get('countryName').countryName)
        countryPopulation = countryDetails.countryPopulation
        countryArea = countryDetails.countryArea
        totalCityPopulation = City.objects.filter(countryName = data.get('countryName').countryName).aggregate(Sum('cityPopulation'))
        if totalCityPopulation['cityPopulation__sum'] == None:
            totalCityPopulation = data.get('cityPopulation')
        else:
            totalCityPopulation = totalCityPopulation['cityPopulation__sum'] + data.get('cityPopulation')
        totalCityArea = City.objects.filter(countryName = data.get('countryName').countryName).aggregate(Sum('cityArea'))
        if totalCityArea['cityArea__sum'] == None:
            totalCityArea = data.get('cityArea')
        else:
            totalCityArea = totalCityArea['cityArea__sum'] + data.get('cityArea')
        if countryPopulation >=  totalCityPopulation and countryArea >=  totalCityArea:
            return data
        elif countryPopulation <=  totalCityPopulation:
            raise serializers.ValidationError('Total of City population is greater than Country population')
        elif countryArea <=  totalCityArea:
            raise serializers.ValidationError('Total of City area is greater than Country area')
        else:
            raise serializers.ValidationError('Invalid data')
