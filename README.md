# Geographical-Vector

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
###### Reference: https://www.postgresql.org/
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
