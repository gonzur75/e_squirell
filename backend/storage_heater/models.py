from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class StorageHeater(models.Model):
    time_stamp = models.DateTimeField(help_text='Time of taking record', primary_key=True, unique=True,
                                      auto_now_add=True)
    relay_one = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    relay_two = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    relay_three = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    relay_four = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    relay_five = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    relay_six = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    temp_one = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    temp_two = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    temp_three = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    temp_four = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])

    def __str__(self):
        return f'Storage heater status at {self.time_stamp}'
