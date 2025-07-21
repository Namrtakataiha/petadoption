from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Extending default User model to include is_admin field
# c# Custom User model with extra fields
class User(AbstractUser):
     mobile_no = models.CharField(max_length=15, blank=True, null=True)
     address = models.TextField(blank=True, null=True)
     is_verified = models.BooleanField(default=False)
     is_admin = models.BooleanField(default=False)
     email = models.EmailField(unique=True)

class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    


    # temp_username = models.CharField(max_length=150, null=True, blank=True)
    # temp_email = models.EmailField(null=True, blank=True)
    # temp_password = models.CharField(max_length=255, null=True, blank=True)
    # temp_mobile_no = models.CharField(max_length=15, null=True, blank=True)
    # temp_address = models.TextField(null=True, blank=True)
    # is_admin = models.BooleanField(default=False)
# Pet category model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Pet model to store pet details
class Pet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pets/', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Adoption application model
class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pet.name} - {self.status}"
