import datetime
import random

from django.core.management.base import BaseCommand

from app_users import models


class Command(BaseCommand):
    """
    Класс для заполонения базы случайными блогерами.
    """
    help = 'create blogers'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.news_list = []

    def add_arguments(self, parser):
        """
        Добавление аргумента общего колличества блогеров, которых необходимо добавить.
        """
        parser.add_argument('total', type=int, help=u'Количество новых записей')
        parser.add_argument('start_username', type=str, help=u'Стартовое значение имени пользователя')

    def handle(self, *args, **kwargs):
        total_users = kwargs['total']
        start_username = kwargs['start_username']

        start_implant = datetime.datetime.now()
        self.stdout.write(f"Началось добавление записей {start_implant}")

        total_created_users = self.create_users(total_users, start_username)

        time_interval = datetime.datetime.now() - start_implant
        self.stdout.write(f"Добавлено {total_created_users} новых записей за {time_interval.seconds} секунд")

    def create_users(self, total_users, start_username):
        """
        Добавление пользователей по одному в базу данных.
        """
        total_created_users = 0

        for user_number in range(total_users):
            username = f'{start_username}_{user_number}'
            print(username)
            try:
                user_obj = models.CustomUser(username=username,
                                             email=f'{username}@mail.ru',
                                             telephone_number=random.randint(0,
                                                                             9999999999999999), )
                user_obj.set_password('123qweQWE')
                user_obj.save()
                total_created_users += 1
            except Exception as exc:
                print(exc)

        return total_created_users
