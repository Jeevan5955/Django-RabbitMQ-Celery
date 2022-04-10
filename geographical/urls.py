from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('continents/', views.ContinentList.as_view()),
    path('continents/<str:continentName>/', views.ContinentDetail.as_view()),
    path('country/', views.CountryList.as_view()),
    path('country/<str:countryName>/', views.CountryDetail.as_view()),
    path('city/', views.CityList.as_view()),
    path('city/<str:cityName>/', views.CityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)