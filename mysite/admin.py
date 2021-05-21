from django.contrib import admin
from .models import Blood_Group,Blood_Records, Hospital, PUser, Location, Donor, Requests, User_Requests, Blood_Bank
# Register your models here.
admin.site.register(Blood_Group)
admin.site.register(Blood_Records)
admin.site.register(Hospital)
admin.site.register(PUser)
admin.site.register(Location)
admin.site.register(Donor)
admin.site.register(Requests)
admin.site.register(User_Requests)
admin.site.register(Blood_Bank)
