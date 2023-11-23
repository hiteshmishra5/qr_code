from django.db import models

class Coordinator(models.Model):
    registration_type_id = models.IntegerField(default=None)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.first_name
