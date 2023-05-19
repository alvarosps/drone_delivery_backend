# Drone Delivery - Backend

This repository contains the backend of the Drone Delivery application. This application allows users to calculate the fastest path and time for a drone to pick up and deliver a package.
## Features

The backend application offers two main features:

- Calculate fastest path and time: Given a drone's current location, a pickup location, and a delivery location, the application calculates the fastest path and time for the drone to pick up and deliver the package.
- Retrieve trip history: The application keeps a history of the last 10 trips calculated, which can be retrieved via the trip_history API endpoint.

## Technologies

The backend is developed in Django, using Django REST framework. It connects to a PostgreSQL database.
## Installation

These instructions assume you have python3, pip and virtualenv installed on your machine.

1. Clone the repository

`git clone https://github.com/your-repo-url/drone_delivery.git`
`cd drone_delivery`

2. Create a Python virtual environment and activate it

`virtualenv env`
`source env/bin/activate`

3. Install the dependencies

`pip install -r requirements.txt`

4. Setup the database
#### OBS: You need to create the DATABASE, USER, PASSWORD in your local postegresql, and modify it on the ./drone_delivery/settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'drone_delivery', #change to your created database
        'USER': 'postgres', #change to your created user
        'PASSWORD': '123456', #change to your created user password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
`python manage.py makemigrations`
`python manage.py migrate`

5. Run the server

`python manage.py runserver`

## Usage

There are two main endpoints:

- POST /api/drone/: Accepts a JSON payload with drone_position, pickup_position and delivery_position, and returns the fastest path and time for the drone.

- GET /api/trip_history/: Returns a list of the last 10 trips calculated.

## Testing

You can run the unit tests by running:

`python manage.py test`
