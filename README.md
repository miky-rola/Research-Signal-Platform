# Research Signal Platform API

## A research signal platform that allows users to receive, analyze, and track options trading signals. Users can view signals, mark them as taken/watching/passed, and track their performance.

## Research Signal Platform  API with django

## Set up environment and run

1. Make sure Python 3.9 and virtualenv are already installed.


`$ python -m venv env`

`$ source env/bin/activate for mac or env\scripts\activate for windows`

`$ pip install -r requirements.txt`

3. Set up environment variables. Examples exist in `.env.sample`:

`cp .env.sample .env`

4. Edit .env to reflect your local environment settings and export them to your terminal

`(env) $ source .env `

5. Run the initial migrations, build the database, create user and run project

`(env) $ python manage.py migrate`

`(env) $ python manage.py createsuperuser`

`(env) $ python manage.py runserver`

## Contribution
1. Create a new branch off the main branch.
2. Make your changes.
3. Push the new branch to github and create a PR to the main branch

![Build Status](https://github.com/CalabasHe/calabashe-api/actions/workflows/ci.yml/badge.svg?branch=main&label=Build%20Status&style=flat-square)
