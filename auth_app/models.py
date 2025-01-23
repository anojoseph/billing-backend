from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    def save(self, *args, **kwargs):
        if self.is_superuser and not self.role_id:
            default_role, created = Role.objects.get_or_create(name='Admin')
            self.role = default_role
        super().save(*args, **kwargs)

    def clean(self):
        if not self.username:
            raise ValidationError("Username is required for staff members")


    def __str__(self):
        return f"{self.username} - {self.role.name}"

    class Meta:
        ordering = ['username']

class Customer(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile_number

    class Meta:
        ordering = ['-created_at']




# import uuid
# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class Role(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return self.name


# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # For OTP users
#     otp_code = models.CharField(max_length=6, blank=True, null=True)  # Temporary OTP storage
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)  # Foreign key to Role model
#     # The username will still be unique across the system
#     username = models.CharField(max_length=150, unique=True, null=True, blank=True)  

#     USERNAME_FIELD = 'username'  # This will be used for login
#     REQUIRED_FIELDS = []  # No required fields when creating via admin
    
#     def save(self, *args, **kwargs):
#         # If the user is a superuser or not in a role, skip phone number check
#         if self.is_superuser or (self.role and self.role.name in ['kitchen', 'waiter', 'cashier']):
#             # Ensure username is provided for kitchen, waiter, cashier roles
#             if self.role and self.role.name in ['kitchen', 'waiter', 'cashier'] and not self.username:
#                 raise ValueError("Username must be provided for kitchen, waiter, cashier users.")
#         else:
#             # If the user is an OTP user, set username as phone number
#             if self.phone_number:
#                 self.username = self.phone_number
#             else:
#                 raise ValueError("Phone number must be provided for OTP users.")

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.phone_number if self.phone_number else self.username