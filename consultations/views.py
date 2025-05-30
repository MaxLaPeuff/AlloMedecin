from django.shortcuts import render
from consultations.models import Consultation, RendezVous, DisponibiliteMedecin
from users.models import Medecin, Patient
import smtplib
import logging

logger = logging.getLogger(__name__)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now, make_aware, is_naive
from datetime import datetime
from django.urls import reverse

from consultations.serializers import RendezVousSerializer, DisponibiliteMedecinSerializer
from users.serializers import MedecinSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import datetime
import json
import datetime



class MedecinDisponibiliteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Obtenir les disponibilités d'un médecin",
        operation_description="Récupère les informations d'un médecin et ses disponibilités.",
        responses={
            200: openapi.Response(
                description="Données du médecin et ses disponibilités",
                examples={
                    "application/json": {
                        "id": 1,
                        "nom": "Dupont",
                        "prenom": "Jean",
                        "specialite": "Cardiologie",
                        "email": "jean.dupont@example.com",
                        "disponibilites": [
                            {"jour": "lundi", "heure_debut": "08:00:00", "heure_fin": "12:00:00"}
                        ]
                    }
                }
            ),
            404: "Médecin non trouvé"
        }
    )
    def get(self, request, *args, **kwargs):
        medecin_id = kwargs.get('id_medecin')
        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            return Response({"error": "Médecin non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        disponibilites = DisponibiliteMedecin.objects.filter(medecin=medecin)
        disponibilites_data = DisponibiliteMedecinSerializer(disponibilites, many=True).data

        for disponibilite in disponibilites_data:
            disponibilite['heure_debut'] = disponibilite['heure_debut'].strftime('%H:%M:%S')
            disponibilite['heure_fin'] = disponibilite['heure_fin'].strftime('%H:%M:%S')

        medecin_data = MedecinSerializer(medecin).data
        medecin_data['disponibilites'] = disponibilites_data

        return Response(medecin_data, status=status.HTTP_200_OK)

# AU niveau de cette vu , le patient demande un rendez-vous à un docteur de son choix
class RendezVousView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Demander un rendez-vous",
        operation_description="Permet à un patient de demander un rendez-vous avec un médecin.",
        request_body=RendezVousSerializer,
        responses={
            201: "Demande de rendez-vous envoyée avec succès.",
            400: "Erreur de validation ou médecin indisponible.",
            404: "Médecin non trouvé."
        }
    )
    def post(self, request, *args, **kwargs):
        medecin_id = kwargs.get('id_medecin')
        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            return Response({"error": "Médecin non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        patient = request.user
        data = request.data.copy()
        data['medecin'] = medecin.id
        data['patient'] = patient.id

        serializer = RendezVousSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        date_rdV = serializer.validated_data['date_heure']
        if is_naive(date_rdV):
            date_rdV = make_aware(date_rdV)

        # Vérification de la disponibilité du médeci_rdVn
        if RendezVous.objects.filter(medecin=medecin, date_heure=date_rdV, statut='Confirme').exists():

            return Response({"error": "Le médecin a déjà un rendez-vous confirmé à cette date"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification des horaires de disponibilité
        # jour = date.strftime('%A').lower()
        # heure = date.time()

        # if not DisponibiliteMedecin.objects.filter(
        #     medecin=medecin,
        #     jour=jour,
        #     heure_debut__lte=heure,
        #     heure_fin__gte=heure
        # ).exists():
        #     return Response({"error": "Le médecin n'est pas disponible à cette heure"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Vérification des horaires de disponibilité
        
        
    


    # S'assurer que jour est bien de type datetime.date
    
        jour_rdv = date_rdV.date()  # Extraire uniquement la date
        heure_rdv = date_rdV.time()  # Extraire uniquement l'heure
       
        # # S'assurer que `jour` est bien de type `datetime.date`
        # if isinstance(jour, str):
        #     jour = datetime.strptime(jour, '%Y-%m-%d').date()

        # Vérifier si une disponibilité correspond au jour et à l'heure
        if not DisponibiliteMedecin.objects.filter(
                medecin=medecin,
                jour=jour_rdv,  # Comparer la date exacte
                heure_debut__lte=heure_rdv,  # L'heure de début doit être inférieure ou égale à l'heure du rendez-vous
                heure_fin__gte=heure_rdv  # L'heure de fin doit être supérieure ou égale à l'heure du rendez-vous
            ).exists():
            return Response({"error": "Le médecin n'est pas disponible à cette heure"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # Création de la demande de rendez-vous

        rendez_vous = serializer.save(statut='En_attente')

                # Envoi d'une notification au médecin (par email)

        confirm_url = request.build_absolute_uri(
            reverse('consultations:confirm_rendezvous', kwargs={'id': rendez_vous.id, 'action': 'CONFIRME'})
        )
        refuse_url = request.build_absolute_uri(
            reverse('consultations:confirm_rendezvous', kwargs={'id': rendez_vous.id, 'action': 'ANNULE'})
        )

       try:
            send_mail(
                subject="AllôMedecin - Nouvelle demande de rendez-vous",
                message=f"""
                    Vous avez une nouvelle demande de rendez-vous de la part de {patient.username} pour le {date_rdV}.
                    Veuillez confirmer ou refuser en cliquant sur les liens ci-dessous :
                    - Confirmer : {confirm_url}
                    - Refuser : {refuse_url}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[medecin.user.email],
            )
        except smtplib.SMTPException as smtp_error:
            logger.error(f"Erreur SMTP : {smtp_error}")
        except Exception as e:
            logger.error(f"Erreur envoi mail : {e}")


        return Response({"message": "Demande de rendez-vous envoyée avec succès. En attente de confirmation du médecin."}, status=status.HTTP_201_CREATED)

   
# Vue permettant au medecin de confirmer le rendez-vous du patient
class ConfirmRendezVous(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Confirmer ou annuler un rendez-vous",
        operation_description="Permet à un médecin de confirmer ou annuler un rendez-vous.",
        manual_parameters=[
            openapi.Parameter(
                'action',
                openapi.IN_QUERY,
                description="Action à effectuer ('CONFIRME' ou 'ANNULE')",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: "Rendez-vous confirmé ou annulé avec succès.",
            400: "Action non valide.",
            404: "Rendez-vous non trouvé ou non autorisé."
        }
    )
    def get(self, request, *args, **kwargs):
        rendez_vous_id = kwargs.get('id')
        try:
            medecin = Medecin.objects.get(user=request.user)
            rendez_vous = RendezVous.objects.get(id=rendez_vous_id, medecin=medecin)
        except Medecin.DoesNotExist:
            return Response({"error": "Vous n'êtes pas un médecin."}, status=status.HTTP_403_FORBIDDEN)
        except RendezVous.DoesNotExist:
            return Response({"error": "Rendez-vous non trouvé ou vous n'êtes pas autorisé à le modifier"}, status=status.HTTP_404_NOT_FOUND)

        action = kwargs.get('action')
        if action == 'CONFIRME':

            rendez_vous.statut = 'Confirme'

            rendez_vous.save()
            # Notification au patient
            send_mail(
                subject="Rendez-vous confirmé",
                message=f"Votre rendez-vous avec le Dr. {rendez_vous.medecin.user.username} pour le {rendez_vous.date} a été confirmé.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rendez_vous.patient.user.email],
            )
            return Response({"message": "Rendez-vous confirmé avec succès."}, status=status.HTTP_200_OK)
        elif action == 'ANNULE':
            rendez_vous.status = 'CANCELLED'
            rendez_vous.save()
            # Notification au patient
            send_mail(
                subject="Rendez-vous refusé",

                message=f"Votre rendez-vous avec le Dr. {rendez_vous.medecin.user.username} pour le {rendez_vous.date_heure} a été refusé.",

                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rendez_vous.patient.user.email],
            )
            return Response({"message": "Rendez-vous refusé avec succès."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Action non valide"}, status=status.HTTP_400_BAD_REQUEST)

class CreateDisponibiliteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Créer des créneaux de disponibilité",
        operation_description="Permet à un médecin de créer ses créneaux de disponibilité.",
        request_body=DisponibiliteMedecinSerializer,
        responses={
            201: "Créneaux de disponibilité créés avec succès.",
            400: "Erreur de validation.",
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'medecin'):
            return Response({"error": "Seuls les médecins peuvent créer des créneaux de disponibilité."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['medecin'] = user.medecin.id

        serializer = DisponibiliteMedecinSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Créneaux de disponibilité créés avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientRendezVousHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Historique des rendez-vous pour un patient",
        operation_description="Permet à un patient de consulter l'historique de ses rendez-vous.",
        responses={
            200: "Historique des rendez-vous récupéré avec succès.",
            403: "Accès refusé."
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'patient'):
            return Response({"error": "Seuls les patients peuvent accéder à cet historique."}, status=status.HTTP_403_FORBIDDEN)

        rendezvous = RendezVous.objects.filter(patient=user.patient).order_by('-date_heure')
        data = RendezVousSerializer(rendezvous, many=True).data

        for rendez_vous in data:
            rendez_vous['date_heure'] = rendez_vous['date_heure'].strftime('%Y-%m-%d %H:%M:%S')

        return Response(data, status=status.HTTP_200_OK)


class MedecinRendezVousHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Historique des rendez-vous pour un médecin",
        operation_description="Permet à un médecin de consulter l'historique de ses rendez-vous.",
        responses={
            200: "Historique des rendez-vous récupéré avec succès.",
            403: "Accès refusé."
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'medecin'):
            return Response({"error": "Seuls les médecins peuvent accéder à cet historique."}, status=status.HTTP_403_FORBIDDEN)

        rendezvous = RendezVous.objects.filter(medecin=user.medecin).order_by('-date_heure')
        data = RendezVousSerializer(rendezvous, many=True).data

        for rendez_vous in data:
            rendez_vous['date_heure'] = rendez_vous['date_heure'].strftime('%Y-%m-%d %H:%M:%S')

        return Response(data, status=status.HTTP_200_OK)


