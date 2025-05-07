from rest_framework import serializers
from django.utils.timezone import make_aware, is_naive
from .models import RendezVous, DisponibiliteMedecin, Consultation
from users.models import Patient, Medecin
from users.serializers import PatientSerializer, MedecinSerializer
from datetime import datetime

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model = RendezVous
        fields = '__all__'

    def validate_date_heure(self, value):
        if is_naive(value):
            value = make_aware(value)
        if value < self.get_current_datetime():
            raise serializers.ValidationError("La date et l'heure doivent être dans le futur.")
        return value

    def get_current_datetime(self):
        # Récupérer la date et l'heure actuelles
        # en tenant compte du fuseau horaire
        # et en s'assurant qu'elles sont conscientes
        # (aware) si le paramètre USE_TZ est activé
        current_datetime = datetime.now()
        if is_naive(current_datetime):
            current_datetime = make_aware(current_datetime)
        return current_datetime

class DisponibiliteMedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibiliteMedecin
        fields = '__all__'

    def validate(self, data):
        # Rendre les heures conscientes si elles sont naïves
        if is_naive(data['heure_debut']):
            data['heure_debut'] = make_aware(data['heure_debut'])
        if is_naive(data['heure_fin']):
            data['heure_fin'] = make_aware(data['heure_fin'])

        # Appeler la méthode clean pour effectuer des validations supplémentaires
        self.clean(data)

        # Validation synchrone pour vérifier les conflits d'horaires
        if self.check_conflict(data):
            raise serializers.ValidationError("Conflit avec une autre disponibilité.")
        return data

    def clean(self, data):
        # Vérifier que les heures de début et de fin sont renseignées
        if data['heure_debut'] is None or data['heure_fin'] is None:
            raise serializers.ValidationError("Les heures de début et de fin doivent être renseignées.")

        # Vérifier que l'heure de début est inférieure à l'heure de fin
        if data['heure_debut'] >= data['heure_fin']:
            raise serializers.ValidationError("L'heure de début doit être inférieure à l'heure de fin.")

        # Vérifier les contraintes spécifiques au dimanche
        if data['jour'].strftime('%A').lower() == 'dimanche':
            if data['heure_debut'] < datetime.time(9, 0) or data['heure_fin'] > datetime.time(17, 0):
                raise serializers.ValidationError(
                    "Le médecin ne peut pas être disponible le dimanche en dehors des heures de 9h à 17h."
                )

    def check_conflict(self, data):
        return DisponibiliteMedecin.objects.filter(
            medecin=data['medecin'],
            jour=data['jour'],
            heure_debut__lt=data['heure_fin'],
            heure_fin__gt=data['heure_debut']
        ).exists()

class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()  # Utilisation du PatientSerializer
    medecin = MedecinSerializer()  # Utilisation du MedecinSerializer

    class Meta:
        model = Consultation
        fields = '__all__'

    def validate_duree(self, value):
        # Exemple de validation synchrone pour la durée
        if value.total_seconds() <= 0:
            raise serializers.ValidationError("La durée doit être positive.")
        return value
