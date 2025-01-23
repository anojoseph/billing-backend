from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import Role

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate default roles and users'

    def handle(self, *args, **options):
        # Create default roles
        default_roles = ['kitchen', 'waiter', 'cashier']
        
        for role_name in default_roles:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created role: {role_name}')
                )
            
            # Create default user for each role
            user, created = User.objects.get_or_create(
                username=role_name,
                defaults={
                    'role': role,
                    'is_staff': True
                }
            )
            
            if created:
                user.set_password(role_name)  # Set password same as username
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {role_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {role_name} already exists')
                )