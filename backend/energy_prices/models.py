from django.db import models


class EnergyPrices(models.Model):
    valid_from = models.DateTimeField(primary_key=True, editable=False, help_text='Time at which given price starts')
    valid_to = models.DateTimeField(editable=False, help_text='Time at which given price stops')
    value_inc_vat = models.DecimalField(max_digits=4,
                                        decimal_places=2,
                                        editable=False,
                                        help_text='energy price per kwh, with Vat',
                                        verbose_name='Price per kwh'
                                        )
