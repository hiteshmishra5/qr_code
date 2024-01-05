from django.db import models
from store.models.customer import Users

class Vitals(models.Model):
    patient = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='vitals_results')
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    BP = models.CharField(max_length=100)
    Oxygen_Saturation = models.CharField(max_length=100)
    BMI = models.CharField(max_length=10)
    Pulse = models.CharField(max_length=10)

    def __str__(self):
        return self.patient