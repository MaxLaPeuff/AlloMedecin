from django.urls import path
from consultations.views import *

app_name = 'consultations'

urlpatterns = [
    
    path('rendezvous/<int:id_medecin>/', RendezVousView.as_view(), name='create_rendezvous'),
    
   
    path('rendezvous/<int:id>/<str:action>/', ConfirmRendezVous.as_view(), name='confirm_rendezvous'),

    path('disponibilites/create/', CreateDisponibiliteView.as_view(), name='create_disponibilite'),

    path('rendezvous/history/patient/', PatientRendezVousHistoryView.as_view(), name='patient_rendezvous_history'),

    path('rendezvous/history/medecin/', MedecinRendezVousHistoryView.as_view(), name='medecin_rendezvous_history'),

]
