from django.db import models


class EnergyPrice(models.Model):
    valid_from = models.DateTimeField(help_text='Time at which given price starts', unique=True)
    valid_to = models.DateTimeField(help_text='Time at which given price stops', unique=True)
    value_inc_vat = models.DecimalField(max_digits=8,
                                        decimal_places=3,
                                        help_text='energy price per kwh, with Vat',
                                        verbose_name='Price per kwh'
                                        )

    def __str__(self):
        return f'Energy price from {self.valid_from} to {self.valid_to}'
