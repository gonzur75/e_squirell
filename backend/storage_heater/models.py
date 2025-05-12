from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StorageHeater(models.Model):
    time_stamp = models.DateTimeField(help_text='Time of taking record', primary_key=True, unique=True,
                                      auto_now_add=True)
    relay_one = models.BooleanField(default=False)
    relay_two = models.BooleanField(default=False)
    relay_three = models.BooleanField(default=False)
    relay_four = models.BooleanField(default=False)
    relay_five = models.BooleanField(default=False)
    relay_six = models.BooleanField(default=False)
    temp_one = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    temp_two = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    temp_three = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    temp_four = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])

    class Meta:
        ordering = ["-time_stamp"]

    def __str__(self):
        return f'Storage heater status at {self.time_stamp}'

    def __repr__(self):
        attrs = ', '.join(f'{key}={repr(value)}' for key, value in vars(self).items())
        return f"{type(self).__name__}({attrs})"
