# Suade Coding Challenge

## Design

Django Rest Framework implementation using an SQLLite DB to store the imported data for processing.

Solution does everything except giving back data per product

## Quickstart

Install packages

`pip install -r requirements.txt`

Initialise the database with the schema:

`python manage.py migrate`

and then run the server

`python manage.py runserver`

The endpoint is available under: e.g. http://127.0.0.1:8000/shop/summary/?date=20190802

> Note: The date is a string in the format YYYmmdd

You will need to import the data before you use it e.g.

`python manage.py import_data -d shop/data/`

## Tests

Basic test for single case (should have more but ran out of time)

`python manage.py tests tests.test_summary`
