
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize project and create default admin user with login=admin and password=bildung'

    def handle(self, *args, **kwargs):
        # Применение всех миграций
        self.stdout.write("Applying migrations...")
        call_command('migrate')

        # Проверяем, существует ли пользователь с логином admin
        if not User.objects.filter(username='admin').exists():
            self.stdout.write("Creating admin user...")
            User.objects.create_superuser(
                username='admin', password='bildung', email='admin@example.com')
            self.stdout.write(self.style.SUCCESS(
                "Admin user created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists."))
