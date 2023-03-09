import os
import json

from django.core.management.base import CommandError
from django.core.management.commands import loaddata
from django.conf import settings

from apps.base.fixtures import users_data, products_data, categories_data


FIXTURE_DIR = os.path.join(settings.BASE_DIR, 'fixtures')
data = users_data + products_data + categories_data


class Command(loaddata.Command):
    help = 'genarate initial data for db (users, products, categories) in format json'

    def handle(self, *args, **options):
        if not FIXTURE_DIR in settings.FIXTURE_DIRS:
            raise CommandError("Please add a list of FIXTURE_DIRS in the settings.py file with the value: %s" % FIXTURE_DIR)
        
        if not os.path.exists(FIXTURE_DIR):
            os.mkdir(FIXTURE_DIR)

        with open(f"{FIXTURE_DIR}/initial_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        
        super().handle(*args, **options)

        try:
            os.remove(f"{FIXTURE_DIR}/initial_data.json")
            os.rmdir(FIXTURE_DIR)
        except:
            pass
