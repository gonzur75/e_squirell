from django.db import models

# Create your models here.
class ProjectSettings(models.Model):
    voltage_threshold = models.SmallIntegerField(default=2495)
    safe_voltage_threshold = models.SmallIntegerField(default=2460)
    heating_required = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # ensure singleton settings
        if db_object := type(self).objects.first():
            self.pk = db_object.pk
        super().save(*args, **kwargs)

