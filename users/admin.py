from django.contrib import admin
from .models import User, Specialite, Patient, Medecin, Pharmacien

admin.site.register(User)
admin.site.register(Specialite)
admin.site.register(Patient)
admin.site.register(Medecin)
admin.site.register(Pharmacien)
