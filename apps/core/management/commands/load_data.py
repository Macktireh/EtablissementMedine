import json
import os
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import CommandError
from django.core.management.commands import loaddata
from tqdm import tqdm

from apps.core.fixtures import data

User = get_user_model()
FIXTURE_DIR = os.path.join(settings.BASE_DIR, "fixtures")


class Command(loaddata.Command):
    help = "genarate initial data for db (users, products, categories) in format json"

    def handle(self, *args: tuple[Any, ...], **options):
        if FIXTURE_DIR not in settings.FIXTURE_DIRS:
            raise CommandError(
                "Please add a list of FIXTURE_DIRS in the settings.py file with the value: %s" % FIXTURE_DIR
            )

        if not os.path.exists(FIXTURE_DIR):
            os.mkdir(FIXTURE_DIR)

        with open(f"{FIXTURE_DIR}/initial_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        super().handle(*args, **options)

        for user in tqdm(User.objects.all()):
            if not user.is_superuser:
                user.set_password(user.password)
                user.save()
