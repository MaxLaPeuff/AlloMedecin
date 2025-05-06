from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientRegisterSerializer, MedecinRegisterSerializer, PharmacienRegisterSerializer, SpecialiteSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.generics import CreateAPIView
from .models import User, Patient, Medecin, Pharmacien , Specialite
from rest_framework import serializers
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from .serializers import MedecinSerializer, PharmacienSerializer
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# ========================== Connexion ===============================
class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="Connexion de l'utilisateur",
        operation_description="Permet à un utilisateur (patient, médecin ou pharmacien) de se connecter à la plateforme.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nom d\'utilisateur'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Mot de passe'),
            }
        ),
        responses={
            200: openapi.Response(description="Connexion réussie"),
            400: openapi.Response(description="Identifiants invalides")
        },
        tags=['Authentification']
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Connexion réussie", "username": user.username}, status=status.HTTP_200_OK)
        return Response({"message": "Identifiants invalides"}, status=status.HTTP_400_BAD_REQUEST)

# ========================== Déconnexion ===============================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Déconnexion de l'utilisateur",
        operation_description="Déconnecte l'utilisateur actuellement connecté.",
        responses={200: openapi.Response(description="Déconnexion réussie")},
        tags=['Authentification']
    )
    def post(self, request):
        logout(request)
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    
class SpecialiteListView(ListAPIView):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    
class SpecialiteCreateView(CreateAPIView):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer

# ========================== Liste des Médecins ===============================
class MedecinListView(ListAPIView):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer

# ========================== Liste des Pharmaciens ===============================
class PharmacienListView(ListAPIView):
    queryset = Pharmacien.objects.all()
    serializer_class = PharmacienSerializer

# ========================== Inscription Patient ===============================
class PatientRegisterView(APIView):
    @swagger_auto_schema(
        request_body=PatientRegisterSerializer,
        responses={201: "Patient inscrit avec succès", 400: "Erreur de validation"},
        operation_description="Permet à un patient de s'inscrire sur la plateforme.",
        tags=['Inscription']
    )
    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient inscrit avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========================== Inscription Médecin ===============================
class MedecinRegisterView(APIView):
    @swagger_auto_schema(
        request_body=MedecinRegisterSerializer,
        responses={201: "Médecin inscrit avec succès", 400: "Erreur de validation"},
        operation_description="Permet à un médecin de s'inscrire sur la plateforme.",
        tags=['Inscription']
    )
    def post(self, request):
        serializer = MedecinRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Médecin inscrit avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========================== Inscription Pharmacien ===============================
class PharmacienRegisterView(APIView):
    @swagger_auto_schema(
        request_body=PharmacienRegisterSerializer,
        responses={201: "Pharmacien inscrit avec succès", 400: "Erreur de validation"},
        operation_description="Permet à un pharmacien de s'inscrire sur la plateforme.",
        tags=['Inscription']
    )
    def post(self, request):
        serializer = PharmacienRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Pharmacien inscrit avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========================== Profil Patient ===============================
class PatientProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PatientRegisterSerializer

    @swagger_auto_schema(
        operation_summary="Récupérer le profil du patient",
        responses={200: PatientRegisterSerializer},
        tags=['Profil']
    )
    def get_object(self):
        return self.request.user.patient

# ========================== Profil Médecin ===============================
class MedecinProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedecinRegisterSerializer

    @swagger_auto_schema(
        operation_summary="Récupérer le profil du médecin",
        responses={200: MedecinRegisterSerializer},
        tags=['Profil']
    )
    def get_object(self):
        return self.request.user.medecin

# ========================== Profil Pharmacien ===============================
class PharmacienProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PharmacienRegisterSerializer

    @swagger_auto_schema(
        operation_summary="Récupérer le profil du pharmacien",
        responses={200: PharmacienRegisterSerializer},
        tags=['Profil']
    )
    def get_object(self):
        return self.request.user.pharmacien

# ========================== Mise à jour de profil ===============================
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
            update_session_auth_hash(self.context.get('request'), instance)
        instance.save()
        return instance

class PatientProfileUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user.patient

class MedecinProfileUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user.medecin

class PharmacienProfileUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user.pharmacien

# ========================== Pagination et Recherche Médecins ===============================
class MedecinPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MedecinSearchView(ListAPIView):
    serializer_class = MedecinSerializer
    pagination_class = MedecinPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Nom ou prénom du médecin", type=openapi.TYPE_STRING),
            openapi.Parameter('specialite', openapi.IN_QUERY, description="Nom de la spécialité", type=openapi.TYPE_STRING),
            openapi.Parameter('ville', openapi.IN_QUERY, description="Ville ou adresse du cabinet", type=openapi.TYPE_STRING),
        ],
        operation_summary="Recherche de médecins",
        operation_description="Permet de rechercher des médecins par nom, spécialité ou ville.",
        tags=['Recherche']
    )
    def get_queryset(self):
        queryset = Medecin.objects.all()
        search_name = self.request.query_params.get('name', None)
        search_specialite = self.request.query_params.get('specialite', None)
        search_ville = self.request.query_params.get('ville', None)

        if search_name:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_name) | Q(user__last_name__icontains=search_name)
            )
        if search_specialite:
            queryset = queryset.filter(specialite__nom__icontains=search_specialite)
        if search_ville:
            queryset = queryset.filter(adresse_cabinet__icontains=search_ville)

        return queryset
