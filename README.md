# How to run the project

After you have cloned the repository to your local machine, you can execute the following command to bring up the services using docker compose

> docker-compose up

This will create the postgres container and the api service container.

For the first time, we need to create a Super User. You can do that by following the below steps

In another terminal, SSH into the web app container by

> docker exec -it blog_app_web_1 /bin/sh

Once inside the container, you can use the standard method for creating a superuser in Django.

> python manage.py createsuperuser

Once you have created the super user, you can use this username/password combo for creating the access_token using the GET Token API from the Postman Collection.

