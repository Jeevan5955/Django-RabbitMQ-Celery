# Geographical-Vector

#### Framework: Django Rest Framework
#### Message Broker: RabbitMQ
#### Worker/Consumer: Celery
#### Database : MYSQL
#### Reverse Proxy: Nginx
#### WSGI application server : Gunicorn

## Validation:

The validation that is used in the Django application is Object-level validation. 

DRF enforces data validation in the deserialization process, which is why you need to call is_valid() before accessing the validated data. If the data is invalid, errors are then appended to the serializer's error property and a ValidationError is thrown.

Only if the data during post or update is valid then it is put in a queue from which celery worker will pickup the task and save it to the database.


Object-level validation :

In our case we have to compare fields with one another in order to validate them. This is when you should use the object-level validation approach.

Example:


    from rest_framework import serializers
    from examples.models import Movie


    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'
            
    def validate(self, data):
        if data['us_gross'] > data['worldwide_gross']:
            raise serializers.ValidationError('worldwide_gross cannot be bigger than us_gross')
        return data

## Installation:

### Recommendation:

#### Setup virtual environment

### RabbitMQ Installation:

#### `apt-get install -y erlang`

#### `apt-get install rabbitmq-server`

#### `systemctl enable rabbitmq-server`

#### `systemctl start rabbitmq-server`

### How to run :

##### i) `pip install -r requirements.txt`

##### ii) Database Configuration
###### a) Create a SQL database
###### Reference: https://dev.mysql.com/
###### b) Open setting.py 
###### Path: vector/filled/setting.py
###### b) Add SQL database details

 ```
 DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
```

##### ii) `python manage.py makemigrations`

##### iii) `python manage.py migrate`

##### iv) `python manage.py runserver`

##### v) `Open: http://127.0.0.1:8000/ `

#### Check the status to make sure everything is running smooth:

#### `systemctl status rabbitmq-server`

#### Starting The Worker Process

#### `celery -A vector worker -l info`

#### Reference : https://www.designmycodes.com/python/use-celery-with-django.html


## Database Schema:

![Vector scheme](https://user-images.githubusercontent.com/54932235/162629045-28414b9b-20bd-420a-b75f-3c8d0461fc13.png)


## Deployment :

### i) WSGI application server - Gunicorn:

Gunicorn is a WSGI server

Gunicorn is built so many different web servers can interact with it. It also does not really care what you used to build your web application - as long as it can be interacted with using the WSGI interface.

Gunicorn takes care of everything which happens in-between the web server and your web application. This way, when coding up your a Django application you don’t need to find your own solutions for:

communicating with multiple web servers
reacting to lots of web requests at once and distributing the load
keepiung multiple processes of the web application running




