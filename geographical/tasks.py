from celery import shared_task
from celery.decorators import task
from rest_framework.response import Response
from .models import *
from rest_framework import status
import requests
from datetime import datetime, timedelta
import requests
import json


@shared_task(serializer='json', name='Create and Update of Continent')
def savingContinent(data):
    saving = Continent(**data)
    saving.save()

@shared_task(serializer='json', name='Create and Update of Country')
def savingCountry(data):
    try:
        data['continentName_id'] = data.pop('continentName')
    except:
        pass
    saving = Country(**data)
    saving.save()

@shared_task(serializer='json', name='Create and Update of City')
def savingCity(data):
    try:
        data['countryName_id'] = data.pop('countryName')
    except:
        pass
    saving = City(**data)
    saving.save()