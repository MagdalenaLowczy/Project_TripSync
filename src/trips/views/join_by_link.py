from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Trip, TripInvite


# niezalogowana osoba klika link
# przekierowanie na logowanie (z ?next=)
# po zalogowaniu wraca do zaproszenia
# widzi szczegóły tripu
# akceptuje/odrzuca
# powiadomienie + log lecą przy decyzji

# BRAKUJE opcji rejestracji => jak nie zgubic ?=next w procesie => zmiana w widokach usera =>nie wiem jak??


class TripJoinByLinkView(LoginRequiredMixin, View):
    def get(self, request, token):
        trip = get_object_or_404(Trip, invite_token=token)

        if trip.is_owner(request.user):
            messages.info(request, "You are the owner of this trip.")
            return redirect("trip-detail", pk=trip.pk)

        if trip.is_participant(request.user):
            messages.info(
                request, f"You already are the participant of this trip: {trip.title}"
            )
            return redirect("trip-detail", pk=trip.pk)

        invite, created = TripInvite.objects.get_or_create(
            trip=trip,
            user=request.user,
            defaults={"invited_by": trip.owner, "status": "pending"},
        )

        return redirect("trip-invite-respond", pk=invite.pk)
