from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Guard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Visitor(models.Model):
    name = models.CharField(max_length=100)
    purpose = models.CharField(max_length=200)
    mobile_number = models.BigIntegerField(null=True, blank=True)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    recorded_by = models.ForeignKey(Guard, on_delete=models.SET_NULL, null=True)  # Stores the Guard who recorded the visitor

    def __str__(self):
        return f"{self.name} (Recorded by {self.recorded_by.name if self.recorded_by else 'Unknown'})"


    def save(self, *args, **kwargs):
        # If exit_time is not set, automatically set it 30 minutes after entry_time
        if not self.exit_time:
            self.exit_time = self.entry_time + timedelta(minutes=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
