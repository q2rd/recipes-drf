"""
Команда которая ожидает подьема базы данных,
во избежания краша бэка.
"""
from django.core.management.base import BaseCommand

import time

from psycopg2 import OperationalError as pc2Error
from django.db.utils import OperationalError

WAIT_TIME = 2


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Точка вхождения."""
        self.stdout.write('Ожидание базы данных.')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (pc2Error, OperationalError):

                self.stdout.write(f'База не поднлась, ждем {WAIT_TIME} секунды..')
                time.sleep(WAIT_TIME)
        self.stdout.write(self.style.SUCCESS('База поднялась.'))