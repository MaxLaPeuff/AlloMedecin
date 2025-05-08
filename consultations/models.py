from django.db import models

from users.models import User, Patient, Medecin

from django.db.models import TextChoices
class StatutChoices(TextChoices):
    EN_ATTENTE = 'en_attente', ('En_attente')
    CONFIRME = 'confirme',('Confirmé')
    ANNULE = 'annule', ('Annulé')


# Modèle de Prsie de rensdez-vous

class RendezVous(models.Model):
    patient = models.ForeignKey("users.Patient", on_delete=models.CASCADE)
    medecin = models.ForeignKey("users.Medecin", on_delete=models.CASCADE)
    date_heure = models.DateTimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=StatutChoices, default=StatutChoices.EN_ATTENTE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rendez-vous de {self.patient} avec {self.medecin} le {self.date_heure}"
    
    
from django.core.exceptions import ValidationError
import datetime
    
class DisponibiliteMedecin(models.Model):
    # JOUR_CHOICES = [
    #     ('lundi', 'Lundi'),
    #     ('mardi', 'Mardi'),
    #     ('mercredi', 'Mercredi'),
    #     ('jeudi', 'Jeudi'),
    #     ('vendredi', 'Vendredi'),
    #     ('samedi', 'Samedi'),
    #     ('dimanche', 'Dimanche'),
    # ]
    medecin = models.ForeignKey("users.Medecin", on_delete=models.CASCADE)
    # jour = models.CharField(max_length=10, choices=JOUR_CHOICES)
    jour  = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    def clean(self): 
        if self.heure_debut >= self.heure_fin:
            raise ValidationError("L'heure de début doit être inférieure à l'heure de fin.")
        if self.jour == 'dimanche' and (self.heure_debut < datetime.time(9, 0) or self.heure_fin > datetime.time(17, 0)):
            raise ValidationError("Le médecin ne peut pas être disponible le dimanche en dehors des heures de 9h à 17h.")

    def __str__(self):
        return f"{self.medecin.user.username} - {self.jour} ({self.heure_debut} à {self.heure_fin})"



# Modèle concernant la consultation
class Consultation(models.Model):
    patient = models.ForeignKey("users.Patient", on_delete=models.CASCADE)
    medecin = models.ForeignKey("users.Medecin", on_delete=models.CASCADE)
    date_heure = models.DateTimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=StatutChoices, default=StatutChoices.EN_ATTENTE)
    date = models.DateTimeField(auto_now_add=True)
    duree = models.DurationField()  # Durée de la consultation
    def __str__(self):
        return f"Consultation de {self.patient} avec {self.medecin} le {self.date_heure}"
