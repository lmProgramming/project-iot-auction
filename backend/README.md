# backend

## how to run mosquitto

if mosquitto is not running, backend will work, but no mqtt api calls will work

if on linux:

```sh
sudo systemctl start mosquitto
```

on windows (administrator):

```sh
net start mosquitto
```

## how to run

make sure you are in this directory in terminal (project-iot-auction/backend)

for first time:

```sh
python manage.py migrate
```

to run:

```sh
python manage.py runserver
```

## contributing

JavaScript/TypeScript should be in static/{js or ts}/ directory
would be nice to use TypeScript and run in this directory

```sh
tsc
```

frontend is in HTML and should be in templates/ directory
CSS should be in static/ directory I think
