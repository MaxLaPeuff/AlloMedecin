from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Medecin, Pharmacien, Specialite

# Customisation de l'affichage de User dans l'admin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_medecin', 'is_pharmacien', 'is_staff')
    list_filter = ('is_patient', 'is_medecin', 'is_pharmacien', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rôles', {'fields': ('is_patient', 'is_medecin', 'is_pharmacien')}),
    )

# Patient
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'telephone', 'date_naissance')
    search_fields = ('user__username', 'user__email', 'telephone')

# Médecin
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite', 'numero_ordre', 'adresse_cabinet', 'telephone')
    list_filter = ('specialite',)
    search_fields = ('user__username', 'numero_ordre', 'user__email')

# Pharmacien
class PharmacienAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom_pharmacie', 'adresse_pharmacie', 'telephone')
    search_fields = ('user__username', 'nom_pharmacie')

# Spécialité
class SpecialiteAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

# Enregistrement des modèles dans l'admin
admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Medecin, MedecinAdmin)
admin.site.register(Pharmacien, PharmacienAdmin)
admin.site.register(Specialite, SpecialiteAdmin)
