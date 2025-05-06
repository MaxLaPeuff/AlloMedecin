from django.urls import path
from .views import LoginView, LogoutView, MedecinListView, MedecinProfileUpdateView, MedecinProfileView, MedecinSearchView, PatientProfileUpdateView, PatientProfileView, PatientRegisterView, MedecinRegisterView, PharmacienListView, PharmacienProfileUpdateView, PharmacienProfileView, PharmacienRegisterView, SpecialiteCreateView, SpecialiteListView

urlpatterns = [
    path('register/patient/', PatientRegisterView.as_view(), name='register_patient'),
    path('register/medecin/', MedecinRegisterView.as_view(), name='register_medecin'),
    path('register/pharmacien/', PharmacienRegisterView.as_view(), name='register_pharmacien'),
    
    # Connexion et déconnexion
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Profil utilisateur
    path('profile/patient/', PatientProfileView.as_view(), name='profile_patient'),
    path('profile/medecin/', MedecinProfileView.as_view(), name='profile_medecin'),
    path('profile/pharmacien/', PharmacienProfileView.as_view(), name='profile_pharmacien'),
    
    # Mise à jour du profil utilisateur
    path('profile/patient/update/', PatientProfileUpdateView.as_view(), name='update_profile_patient'),
    path('profile/medecin/update/', MedecinProfileUpdateView.as_view(), name='update_profile_medecin'),
    path('profile/pharmacien/update/', PharmacienProfileUpdateView.as_view(), name='update_profile_pharmacien'),
    
    #Recherche de Medecin par critère 
    path('search/medecins/', MedecinSearchView.as_view(), name='medecin_search'),
    
    path('medecins/', MedecinListView.as_view(), name='medecin_list'),
    path('pharmaciens/', PharmacienListView.as_view(), name='pharmacien_list'),
    
    path('specialites/', SpecialiteListView.as_view(), name='specialite-list'),
    path('specialites/create/', SpecialiteCreateView.as_view(), name='specialite-create'),
    
    ]

