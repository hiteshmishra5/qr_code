from django.contrib import admin
from .models.customer import Users
from .models.Coordinator import Coordinator
from .models.Technician import Technician
from .models.optometry import Optometry
from .models.location import Location


# Register your models here.

admin.site.register(Users)
admin.site.register(Coordinator)
admin.site.register(Technician)
admin.site.register(Optometry)
admin.site.register(Location)
