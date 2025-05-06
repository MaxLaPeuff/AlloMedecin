from rest_framework import serializers
from users.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_patient', 'is_medecin', 'is_pharmacien']

class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = ['id', 'nom']

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'adresse', 'telephone', 'date_naissance']

class MedecinSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    specialite = SpecialiteSerializer()

    class Meta:
        model = Medecin
        fields = ['id', 'user', 'specialite', 'numero_ordre', 'adresse_cabinet', 'telephone']

class PharmacienSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Pharmacien
        fields = ['id', 'user', 'nom_pharmacie', 'adresse_pharmacie', 'telephone']
