from django.contrib import admin

from energy_prices.models import EnergyPrice


# Register your models here.
class EnergyPriceAdmin(admin.ModelAdmin):
    list_display = (
        'valid_from',
        'valid_to',
        'value_inc_vat'
    )


admin.site.register(EnergyPrice, EnergyPriceAdmin)
