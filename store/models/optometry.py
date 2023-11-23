from django.db import models
from store.models import Users

class Optometry(models.Model):
    patient = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='optometry_results')
    far_vision_right = models.CharField(max_length=10)
    far_vision_left = models.CharField(max_length=10)
    near_vision_right = models.CharField(max_length=10)
    near_vision_left = models.CharField(max_length=10)
    color_vision = models.CharField(max_length=15, default=True, choices=[
        ('NORMAL', 'Normal'),
        ('RED', 'Red'),
        ('GREEN', 'Green'),
        ('RED_GREEN', 'Red-green'),
        ('DEFICIENCY', 'deficiency')
    ])
    others = models.CharField(max_length=300)

    def __str__(self):
        return self.patient


