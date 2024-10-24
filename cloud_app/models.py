from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

class Appointment(models.Model):

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    test = models.ForeignKey('Test', on_delete=models.CASCADE) 
    date = models.DateField(validators=[MinValueValidator(limit_value=timezone.now().date())])
    timing = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.test}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.user.username

class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)  # Link payment to appointment
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  # Ensure this exists
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Payment for {self.appointment.test} by {self.user.username}"
