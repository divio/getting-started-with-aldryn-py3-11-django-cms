# Getting Started with Aldryn Django CMS

[![Deploy to Divio](https://img.shields.io/badge/DEPLOY-TO%20DIVIO-DFFF67?logo=docker&logoColor=white&labelColor=333333)](https://control.divio.com/app/new/?template_url=https://github.com/divio/getting-started-with-aldryn-py3-11-django-cms/archive/refs/heads/main.zip)

This templates enables the Aldryn framework on Divio Cloud. We do not recommend to use this template, use [Getting Started with Django CMS](https://github.com/divio/getting-started-with-django-cms) instead.

## Cloud Setup

Use the app creation wizard with a free [Divio Account](https://control.divio.com/) and choose **Aldryn django CMS** from the template selection. Alternatively, click the `Deploy to Divio` button above and follow the app creation wizard. Finally, deploy your app to the `test` or `live` environment.

Beware that the **admin** user is not created automatically.
You can do so by connecting via SSH and manually run `python manage.py createsuperuser`.

For in-depth details about Divio Cloud, refer to the [Divio documentation](https://docs.divio.com/introduction/).

## Local Setup

Install the [Divio CLI](https://github.com/divio/divio-cli) to set up your app locally.

Alternatively, build this app locally using Docker:

1. Ensure [Docker](https://docs.docker.com/get-docker/) is installed and running.
2. Clone this repository locally.
3. Build the app with `docker compose build`.
4. Run the migrations with `docker compose run --rm web python manage.py migrate`
5. Create a superuser with `docker compose run --rm web python manage.py createsuperuser`
6. Run the app using `docker compose up`.
7. Open [http://localhost:8000]() to view your app.
