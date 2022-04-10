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

   a) communicating with multiple web servers
   
   b) reacting to lots of web requests at once and distributing the load
   
   c) keepiung multiple processes of the web application running
   
#### Configuration of Gunicorn

Create and open a systemd service file for Gunicorn with sudo privileges in your preferred text editor. The service filename should match the socket filename with the exception of the extension:

`sudo nano /etc/systemd/system/webapp.service`

Add the below code and change the respective like service name,path of application and path of gunicorn

Path of application : `pwd`

Path of gunicorn : `which gunicorn`

    [Unit]
    Description=webapp daemon
    After=network.target

    [Service]
    PIDFile=/var/run/webapp.pid
    WorkingDirectory={path of Django application}
    ExecStart={path of gunicorn} --config {path of Django application}/webapp.py --pid /var/run/webapp.pid vector.wsgi:application
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

Reload the daemon to reread the service definition:

    sudo systemctl daemon-reload
    
Then restart the Gunicorn process:

    sudo systemctl restart webapp
    
Similary for webapp1 and webapp2

##### Deploying Celery in production:

Create celery environment file:

    sudo nano /etc/default/vectorceleryd
    
Add the below code and add the path of celery:

Path of celery: `which celery`

    CELERYD_NODES="worker1 worker2"

    # The name of the Celery App, should be the same as the python file
    # where the Celery tasks are defined
    CELERY_APP="vector"

    # Log and PID directories
    CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
    CELERYD_PID_FILE="/var/run/celery/%n.pid"

    # Log level
    CELERYD_LOG_LEVEL=INFO

    # Path to celery binary, that is in your virtual environment
    CELERY_BIN={Path of celery}
    
Creating celery as service:
 
    sudo nano /etc/systemd/system/vectorworker.service
    
Add the below code and add the path of working directory:

    [Unit]
    Description=Celery Service
    After=network.target

    [Service]
    Type=forking
    User=root
    EnvironmentFile=/etc/default/vectorceleryd
    WorkingDirectory={path of working directory}
    ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
      --pidfile=${CELERYD_PID_FILE}'
    ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
      -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

    [Install]
    WantedBy=multi-user.target
    
Reload the daemon to reread the service definition:

    sudo systemctl daemon-reload
    
Then restart the Gunicorn process of celery worker:

    sudo systemctl restart vectorworker


#### ii) Configure Nginx to Proxy Pass: 

Now that Gunicorn is set up, next you’ll configure Nginx to pass traffic to the process.

Installation:

    sudo apt install nginx

Start by creating and opening a new server block in Nginx’s sites-available directory:

    sudo nano /etc/nginx/sites-available/vector

Add the below code and change the repective domain name: 

    upstream vector {
        server 127.0.0.1:8000;
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
    }

    server {
            listen 80;
            server_name www.domain.com ;
            proxy_set_header Access-Control-Allow-Origin *;

            location / {
                proxy_pass http://vector;
                proxy_set_header "Access-Control-Allow-Origin" *;
                proxy_set_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, HEAD, DELETE";
                proxy_set_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept";
                proxy_set_header   X-Real-IP $remote_addr;
                proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header   X-Forwarded-Host $server_name;
                #proxy_set_header   X-Forwarded-Proto https;
            }
    }
    
Next, create a symlink of this Nginx configuration in the sites-enabled folder by running the following command: 
 
    sudo ln -s /etc/nginx/sites-available/vector /etc/nginx/sites-enabled
 
Testing the configuration file: 

    sudo nginx -t 
    
Next, reload your Nginx configurations by running the reload command: 

    sudo service nginx reload
    
Load Balancing Algorithm:

Round Robin – Requests are distributed evenly across the servers, with server weights taken into consideration. This method is used by default.
    
 #### iii) HTTP to HTTPS using Certbot:
 
     sudo apt-get install python3-certbot-nginx 
     sudo certbot --nginx


Nginx Deployment Documentation: [Nginx deployment documentation.pdf](https://github.com/Jeevan5955/Geographical-Vector/files/8459463/Nginx.deployment.documentation.pdf)


## Complete production architecture:


![Vector Complete Arch drawio](https://user-images.githubusercontent.com/54932235/162632239-e90b1b50-e239-493d-9319-a2201260866e.png)




