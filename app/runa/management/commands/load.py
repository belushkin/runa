from django.core.management.base import BaseCommand
from runa.models import Category


class Command(BaseCommand):
    help = 'Load basic categories structure'

    def handle(self, *args, **options):
        c1 = Category(name='test')
        c1.save()

        c2 = Category(name='test2', parent=c1)
        c2.save()

        c3 = Category(name='test3')
        c3.save()

        c4 = Category(name='test4', parent=c3)
        c4.save()

        c5 = Category(name='test5', parent=c4)
        c5.save()

        self.stdout.write(self.style.SUCCESS('Categories added'))
