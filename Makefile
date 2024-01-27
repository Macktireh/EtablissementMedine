.PHONY: runserver m mm mmm sm shell test superuser loaddata dumpdata i18n

.DEFAULT_GOAL := runserver

runserver:
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
	poetry run coverage run --source='.' manage.py test -v 2

coverage:
	poetry run coverage report -m
	poetry run coverage html

testc: test coverage

superuser:
	poetry run python manage.py createsuperuser --email=admin@gmail.com --name=Admin --phone_number=77123456

loaddata:
	poetry run python manage.py load_data db.json

dumpdata:
	poetry run python manage.py dumpdata > db.json

i18n:
	poetry run django-admin makemessages --all --ignore=env

rufffix:
	poetry run ruff --fix --exit-zero .

ruffformat:
	poetry run ruff format .

ruff:
	poetry run ruff check .

clean: rufffix ruffformat ruff
