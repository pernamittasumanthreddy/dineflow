from django.core.management.base import BaseCommand
from apps.accounts.seeder import seed_roles_and_users

class Command(BaseCommand):
    help = 'Seed 10 standard enterprise roles and default staff/guest users'

    def handle(self, *args, **options):
        seed_roles_and_users()
        self.stdout.write(self.style.SUCCESS('Successfully seeded all 10 DineFlow roles and user accounts!'))
