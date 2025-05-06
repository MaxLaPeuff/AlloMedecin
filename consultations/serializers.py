from rest_framework import serializers
from .models import RendezVous, DisponibiliteMedecin, Consultation
from users.models import Patient, Medecin
from users.serializers import PatientSerializer, MedecinSerializer

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '__all__'

    async def validate_date_heure(self, value):
       
        if value < await self.get_current_datetime():
            raise serializers.ValidationError("La date et l'heure doivent être dans le futur.")
        return value

    async def get_current_datetime(self):
        from datetime import datetime
        return datetime.now()

class DisponibiliteMedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibiliteMedecin
        fields = '__all__'

    async def validate(self, data):
        # Validation asynchrone pour vérifier les conflits d'horaires
        if await self.check_conflict(data):
            raise serializers.ValidationError("Conflit avec une autre disponibilité.")
        return data

    async def check_conflict(self, data):
       
        return await DisponibiliteMedecin.objects.filter(
            medecin=data['medecin'],
            jour=data['jour'],
            heure_debut__lt=data['heure_fin'],
            heure_fin__gt=data['heure_debut']
        ).aexists()

class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()  # Utilisation du PatientSerializer
    medecin = MedecinSerializer()  # Utilisation du MedecinSerializer

    class Meta:
        model = Consultation
        fields = '__all__'

    async def validate_duree(self, value):
        # Exemple de validation asynchrone pour la durée
        if value.total_seconds() <= 0:
            raise serializers.ValidationError("La durée doit être positive.")
        return value
