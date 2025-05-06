from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Définition du schéma pour la documentation
schema_view = get_schema_view(
   openapi.Info(
      title="AlloMédecin API",
      default_version='v1',
      description="Documentation des API pour la plateforme AlloMédecin",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@allomedecin.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),          # Pour les utilisateurs
    path('api/consultations/', include('consultations.urls')),  # Pour les consultations
   # path('api/payments/', include('payments.urls')),    # Pour les paiements
   # path('api/notifications/', include('notifications.urls')),  # Pour les notifications
]

