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
from django.utils.timezone import now


class RendezVousView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        medecin_id = kwargs.get('id')
        try:
            medecin = Medecin.objects.get(id=medecin_id)
        except Medecin.DoesNotExist:
            return Response({"error": "Médecin non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        patient = request.user
        date = request.data.get('date')

        # Vérification de la disponibilité du médecin
        if RendezVous.objects.filter(medecin=medecin, date=date, status='CONFIRMED').exists():
            return Response({"error": "Le médecin n'est pas disponible à cette date"}, status=status.HTTP_400_BAD_REQUEST)

        # Création de la demande de rendez-vous
        rendez_vous = RendezVous.objects.create(
            medecin=medecin,
            patient=patient,
            date=date,
            status='PENDING'
        )

        # Envoi d'une notification au médecin (par email)
        send_mail(
            subject="Nouvelle demande de rendez-vous",
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

        action = request.data.get('action')
        if action == 'CONFIRM':
            rendez_vous.status = 'CONFIRMED'
            rendez_vous.save()
            # Notification au patient
            send_mail(
                subject="Rendez-vous confirmé",
                message=f"Votre rendez-vous avec le Dr. {rendez_vous.medecin.username} pour le {rendez_vous.date} a été confirmé.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rendez_vous.patient.email],
            )
            return Response({"message": "Rendez-vous confirmé avec succès."}, status=status.HTTP_200_OK)
        elif action == 'REFUSE':
            rendez_vous.status = 'REFUSED'
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
