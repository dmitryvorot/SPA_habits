docker-compose up --build
docker-compose exec web_api python manage.py migrate
docker-compose exec web_api python manage.py collectstatic