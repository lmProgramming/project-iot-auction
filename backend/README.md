# Backend

## How to run Mosquitto

If Mosquitto is not running, the backend will work, but no MQTT API calls will work.

### On Linux

```sh
sudo systemctl start mosquitto
```

### On Windows (Administrator)

```sh
net start mosquitto
```

## How to run

Make sure you are in this directory in terminal (`project-iot-auction/backend`).

### For the first time

```sh
python manage.py migrate
python manage.py seed
```

### To run

#### Normally

```sh
python manage.py runserver
```

#### On 2 raspberry pi's over the network

on the raspberry that is the server:

```sh
sudo nano /etc/mosquitto/mosquitto.conf
```

add lines:
listener 1883
allow_anonymous true

```sh
sudo systemctl restart mosquitto
hostname -I
```

update the broker IP everywhere to the one from hostname

```sh
python manage.py runserver
```

## Admin panel

because our database is local, you need to create a superuser first
best with the login and password provided below

```sh
py manage.py createsuperuser
```

<http://your-server-ip:8000/admin/>

username: pi
password: P@ssw0rd

## Database (easier to look at it from admin view)

```sh
sudo apt-get install sqlite3 libsqlite3-dev
python3 manage.py dbshell
.tables
```

## More commands

clear database:

```sh
python manage.py clear_db
```

## Contributing

JavaScript/TypeScript should be in the `static/{js, ts}/` directory. It would be nice to use TypeScript and run in this directory:

```sh
tsc
```

The frontend is in HTML and should be in the `templates/` directory. CSS should be in the `static/css` directory.
