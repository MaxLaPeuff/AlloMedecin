from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle personnalisé User
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_medecin = models.BooleanField(default=False)
    is_pharmacien = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Spécialité médicale (ex: cardiologie, pédiatrie, etc.)
class Specialite(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


# Profil Patient
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Profil Médecin
class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medecin')
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)
    numero_ordre = models.CharField(max_length=100)  # numéro d'enregistrement à l'ordre des médecins
    adresse_cabinet = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"Dr {self.user.first_name} {self.user.last_name}"

# Profil Pharmacien
class Pharmacien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacien')
    nom_pharmacie = models.CharField(max_length=255)
    adresse_pharmacie = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    #numero_agrement = models.CharField(max_length=100)  # numéro officiel d'autorisation

    def __str__(self):
        return f"{self.nom_pharmacie} ({self.user.username})"