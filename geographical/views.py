from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from .tasks import *
import json
from datetime import datetime, timedelta
import requests


class ContinentList(APIView):
    """
    List all Contient, or create a new Contient
    """
  
    def get(self, request, format=None):
        contients = Continent.objects.all()
        serializer = ContinentSerializer(contients, many=True)
        return Response(serializer.data)
  
    def post(self, request, format=None):
        serializer = ContinentSerializer(data=request.data)
        if serializer.is_valid():
            savingContinent.delay(request.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class ContinentDetail(APIView):
    """
    Retrieve, update or delete a contient instance
    """
    def get_object(self, continentName):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return Continent.objects.get(pk=continentName)
        except Continent.DoesNotExist:
            raise Http404
  
    def get(self, request, continentName, format=None):
        continents = self.get_object(continentName)
        serializer = ContinentSerializer(continents)
        return Response(serializer.data)
  
    def put(self, request, continentName, format=None):
        continents = self.get_object(continentName)
        serializer = ContinentSerializer(continents, data=request.data)
        if serializer.is_valid():
            savingContinent.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, continentName, format=None):
        continents = self.get_object(continentName)
        serializer = ContinentSerializer(continents,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            savingContinent.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, continentName, format=None):
        continents = self.get_object(continentName)
        serializer = ContinentSerializer(continents,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            savingContinent.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, continentName, format=None):
        contients = self.get_object(continentName)
        contients.delete()
        return Response({'Status':'Deleted'}, status=status.HTTP_200_OK)

class CountryList(APIView):
    """
    List all Country, or create a new Country
    """
  
    def get(self, request, format=None):
        countrys = Country.objects.all()
        serializer = CountrySerializer(countrys, many=True)
        return Response(serializer.data)
  
    def post(self, request, format=None):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            savingCountry.delay(request.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class CountryDetail(APIView):
    """
    Retrieve, update or delete a country instance
    """
    def get_object(self, countryName):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return Country.objects.get(pk=countryName)
        except Country.DoesNotExist:
            raise Http404
  
    def get(self, request, countryName, format=None):
        countrys = self.get_object(countryName)
        serializer = CountrySerializer(countrys)
        return Response(serializer.data)
  
    def put(self, request, countryName, format=None):
        countrys = self.get_object(countryName)
        serializer = CountrySerializer(countrys, data=request.data)
        if serializer.is_valid():
            savingCountry.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, countryName, format=None):
        countrys = self.get_object(countryName)
        serializer = CountrySerializer(countrys,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            savingCountry.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, countryName, format=None):
        countrys = self.get_object(countryName)
        serializer = CountrySerializer(countrys,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            savingCountry.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, countryName, format=None):
        contients = self.get_object(countryName)
        contients.delete()
        return Response({'Status':'Deleted'}, status=status.HTTP_200_OK)

class CityList(APIView):
    """
    List all City, or create a new City
    """
  
    def get(self, request, format=None):
        citys = City.objects.all()
        serializer = CitySerializer(citys, many=True)
        return Response(serializer.data)
  
    def post(self, request, format=None):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            savingCity.delay(request.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class CityDetail(APIView):
    """
    Retrieve, update or delete a city instance
    """
    def get_object(self, cityName):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return City.objects.get(pk=cityName)
        except City.DoesNotExist:
            raise Http404
  
    def get(self, request, cityName, format=None):
        citys = self.get_object(cityName)
        serializer = CitySerializer(citys)
        return Response(serializer.data)
  
    def put(self, request, cityName, format=None):
        citys = self.get_object(cityName)
        serializer = CitySerializer(citys, data=request.data)
        if serializer.is_valid():
            savingCity.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, cityName, format=None):
        citys = self.get_object(cityName)
        serializer = CitySerializer(citys,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            savingCity.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, cityName, format=None):
        citys = self.get_object(cityName)
        serializer = CitySerializer(citys,
                                           data=request.data,
                                           partial=True)
        if serializer.is_valid():
            savingCity.delay(request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, cityName, format=None):
        citys = self.get_object(cityName)
        citys.delete()
        return Response({'Status':'Deleted'}, status=status.HTTP_200_OK)