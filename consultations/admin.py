from django.contrib import admin
from .models import RendezVous, DisponibiliteMedecin, Consultation

# Rendez-vous
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_heure', 'statut', 'date')
    list_filter = ('statut', 'date_heure')
    search_fields = ('patient__user__username', 'medecin__user__username', 'motif')

# Disponibilité Médecin
class DisponibiliteMedecinAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'jour', 'heure_debut', 'heure_fin')
    list_filter = ('jour',)
    search_fields = ('medecin__user__username',)

# Consultation
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_heure', 'statut', 'duree', 'date')
    list_filter = ('statut', 'date_heure')
    search_fields = ('patient__user__username', 'medecin__user__username', 'motif')

# Enregistrement des modèles dans l'admin
admin.site.register(RendezVous, RendezVousAdmin)
admin.site.register(DisponibiliteMedecin, DisponibiliteMedecinAdmin)
admin.site.register(Consultation, ConsultationAdmin)
