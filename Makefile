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
	poetry run pytest

superuser:
	poetry run python manage.py createsuperuser

loaddata:
	poetry run python manage.py load_data

i18n:
	poetry run django-admin makemessages --all --ignore=env

black:
	poetry run python -m black .

isort:
	poetry run python -m isort --profile black .
