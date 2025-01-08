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
python python manage.py seed
```

### To run

```sh
python manage.py runserver
```

### More commands

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
