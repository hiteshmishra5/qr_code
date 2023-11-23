from django.db import models


class Technician(models.Model):
    registration_type_id = models.IntegerField(default=None)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True)
    # allocated_patients = models.ManyToManyField(Patient, blank=True)

    def __str__(self):
        return self.first_name
