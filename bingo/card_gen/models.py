from django.db import models

# Create your models here.
# models.py
from django.db import models
import uuid
import random

class BingoCard(models.Model):
    #serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    serial_number = models.IntegerField(unique=True, editable=False)
    player_name = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField()
    numbers = models.JSONField()  # Stores the card numbers as a JSON object
    is_claimed = models.BooleanField(default=False)
    numbers = models.JSONField()  # Stores the card numbers as a JSON object
    marked_numbers = models.JSONField(default=list)  # Stores the marked numbers


    def save(self, *args, **kwargs):
        if not self.serial_number:
            # Generate a unique number between 1 and 999
            while True:
                number = random.randint(1, 999)  # Generate a number in the desired range
                if not BingoCard.objects.filter(serial_number=number).exists():
                    self.serial_number = number
                    break
        super().save(*args,  **kwargs)
    


    def __str__(self):
        return f"Card {self.serial_number}"
# models.py
from django.db import models

class CalledNumber(models.Model):
    number = models.IntegerField()
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Number {self.number} called at {self.called_at}"