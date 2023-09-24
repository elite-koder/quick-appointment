import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from appointments.services import AppointmentService
from slots.services import SlotService

logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def book_appointment(request):
    if request.method == "GET":
        appointment_date = request.GET.get("appointment_date")
        if not appointment_date:
            appointment_date = timezone.now().date()
        else:
            appointment_date = timezone.datetime.strptime(appointment_date, '%d/%m/%Y').date()
        return render(request, "book_appointment.html", {"page": 'book_appointment',
                                                         "slots": SlotService().get_free_slot_list(request.user,
                                                                                                   appointment_date)})
    elif request.method == "POST":
        slot_id = request.POST["slot_id"]
        if slot_id.isnumeric():
            try:
                AppointmentService().book_appointment(slot_id, request.user)
                messages.success(request, "Hurrah!!! Appointment Booked Successfully")
            except Exception:
                logger.exception("exception while booking appointment")
                messages.error(request, "Hiss!!! Slot is not available anymore")
        else:
            messages.error(request, "Hurrah!!! Please select slot first")
        return redirect(f"/appointments/create?appointment_date={request.POST['appointment_date']}")


@login_required
def manage_appointment(request):
    if request.method == "GET":
        return render(request, "manage_appointment.html", {"page": 'manage_appointment',
                                                           "appointments": AppointmentService().list_guest_appointments(
                                                               request.user)})
    elif request.method == "POST":
        appointment_id = request.POST["appointment_id"]
        if appointment_id.isnumeric():
            try:
                AppointmentService().delete_appointment(appointment_id, request.user)
                messages.success(request, "Hurrah!!! Appointment deleted successfully")
            except Exception:
                logger.exception("exception while deleting appointment")
        else:
            messages.error(request, "Please select an appointment")
        return redirect("/appointments/manage")
