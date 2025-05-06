from django.urls import path
from consultations.views import RendezVousView

app_name = "consultations"

urlpatterns = [
    # Endpoint pour la creation de nouvel rendez-vous
    path('rendezvous/<int:id_medecin>/', RendezVousView.as_view(), name='create_rendezvous'),
    # Endpoint pour la mise à jour du status d'un rendez-vous
    path('rendezvous/update/<int:id>/', RendezVousView.as_view(), name='update_rendezvous'),
]
