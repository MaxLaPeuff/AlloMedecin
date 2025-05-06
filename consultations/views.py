from django.shortcuts import render
from consultations.models import Consultation, RendezVous, DisponibiliteMedecin
from users.models import Medecin, Patient


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now, make_aware, is_naive
from datetime import datetime


class RendezVousView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        medecin_id = kwargs.get('id')
        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            return Response({"error": "Médecin non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        patient = request.user
        date_str = request.data.get('date')

        # Convert the provided date to a timezone-aware datetime object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if is_naive(date):
                date = make_aware(date)
        except ValueError:
            return Response({"error": "Format de date invalide. Utilisez '%Y-%m-%d %H:%M:%S'."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de la disponibilité du médecin
        if RendezVous.objects.filter(medecin=medecin, date=date, status='CONFIRMED').exists():
            return Response({"error": "Le médecin a déjà un rendez-vous confirmé à cette date"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification des horaires de disponibilité
        jour = date.strftime('%A').lower()
        heure = date.time()

        if not DisponibiliteMedecin.objects.filter(
            medecin=medecin,
            jour=jour,
            heure_debut__lte=heure,
            heure_fin__gte=heure
        ).exists():
            return Response({"error": "Le médecin n'est pas disponible à cette heure"}, status=status.HTTP_400_BAD_REQUEST)

        # Création de la demande de rendez-vous
        rendez_vous = RendezVous.objects.create(
            medecin=medecin,
            patient=patient,
            date=date,
            status='EN_ATTENTE'
        )

        # Envoi d'une notification au médecin (par email)
        send_mail(
            subject="AllôMedecin.Nouvelle demande de rendez-vous",
            message=f"Vous avez une nouvelle demande de rendez-vous de la part de {patient.username} pour le {date}. Veuillez confirmer ou refuser.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[medecin.email],
        )

        return Response({"message": "Demande de rendez-vous envoyée avec succès. En attente de confirmation du médecin."}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        rendez_vous_id = kwargs.get('id')
        try:
            rendez_vous = RendezVous.objects.get(id=rendez_vous_id, medecin=request.user)
        except RendezVous.DoesNotExist:
            return Response({"error": "Rendez-vous non trouvé ou vous n'êtes pas autorisé à le modifier"}, status=status.HTTP_404_NOT_FOUND)

        statut = request.data.get('satut')
        if statut == 'CONFIRM':
            rendez_vous.status = 'Comfirmé'
            rendez_vous.save()
            # Notification au patient
            send_mail(
                subject="Rendez-vous confirmé",
                message=f"Votre rendez-vous avec le Dr. {rendez_vous.medecin.username} pour le {rendez_vous.date} a été confirmé.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rendez_vous.patient.email],
            )
            return Response({"message": "Rendez-vous confirmé avec succès."}, status=status.HTTP_200_OK)
        elif statut == 'REFUSE':
            rendez_vous.statut = 'Annulé'
            rendez_vous.save()
            # Notification au patient
            send_mail(
                subject="Rendez-vous refusé",
                message=f"Votre rendez-vous avec le Dr. {rendez_vous.medecin.username} pour le {rendez_vous.date} a été refusé.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rendez_vous.patient.email],
            )
            return Response({"message": "Rendez-vous refusé avec succès."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Action non valide"}, status=status.HTTP_400_BAD_REQUEST)


class MedecinDisponibiliteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        medecin_id = kwargs.get('id')
        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            return Response({"error": "Médecin non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        disponibilites = DisponibiliteMedecin.objects.filter(medecin=medecin).values('jour', 'heure_debut', 'heure_fin')

        medecin_data = {
            "id": medecin.id,
            "nom": medecin.nom,
            "prenom": medecin.prenom,
            "specialite": medecin.specialite,
            "email": medecin.email,
            "disponibilites": list(disponibilites)
        }

        return Response(medecin_data, status=status.HTTP_200_OK)
