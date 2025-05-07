from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import Patient, Medecin, Pharmacien, Specialite

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MedecinSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Medecin
        fields = ['user', 'specialite', 'numero_ordre', 'adresse_cabinet', 'telephone']
        
class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = ['id', 'nom']


        
class PharmacienSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Pharmacien
        fields = ['user', 'nom_pharmacie', 'adresse_pharmacie', 'telephone']

# ================== PATIENT ==================
class PatientRegisterSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Patient

        fields = ['user', 'adresse', 'telephone', 'date_naissance']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_patient=True)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient

# ================== MEDECIN ==================
class MedecinRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Medecin
        fields = ['user', 'specialite', 'numero_ordre', 'adresse_cabinet', 'telephone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_medecin=True)
        medecin = Medecin.objects.create(user=user, **validated_data)
        return medecin

# ================== PHARMACIEN ==================
class PharmacienRegisterSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Pharmacien

        fields = ['user', 'nom_pharmacie', 'adresse_pharmacie', 'telephone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, is_pharmacien=True)
        pharmacien = Pharmacien.objects.create(user=user, **validated_data)
        return pharmacien

