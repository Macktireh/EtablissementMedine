.PHONY: start m mm mmm sm shell test superuser loaddata i18n

.DEFAULT_GOAL := start

start:
	poetry run python manage.py runserver

# migrate
m:
	poetry run python manage.py migrate

# makemigrations
mm:
	poetry run python manage.py makemigrations

# makemigrations + migrate
mmm: mm m

# showmigrations
sm:
	poetry run python manage.py showmigrations

shell:
	poetry run python manage.py shell_plus

test:
	poetry run pytest --cov --cov-report=html:coverage

superuser:
	poetry run python manage.py createsuperuser --email=admin@gmail.com --name=Admin --phone_number=77123456

loaddata:
	poetry run python manage.py load_data

i18n:
	poetry run django-admin makemessages --all --ignore=env

black:
	poetry run python -m black .

isort:
	poetry run python -m isort --profile black .
