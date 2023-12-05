from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100, default=None)
    technician_name = models.CharField(max_length=100, default="Unknown Technician")


    def __str__(self):
        return self.name
