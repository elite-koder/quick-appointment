import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from slots.services import SlotService

logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def create_slot(request):
    if request.method == "GET":
        now = timezone.now()
        test_start_time = now.replace(hour=now.hour+1, minute=0).strftime("%d/%m/%Y %I:%M %p")
        test_end_time = now.replace(hour=now.hour+1, minute=30).strftime("%d/%m/%Y %I:%M %p")
        return render(request, "create_slot.html", {"page": 'create_slot', "test_start_time": test_start_time, "test_end_time": test_end_time})
    elif request.method == "POST":
        start_time = timezone.datetime.strptime(request.POST.get('start_time'), '%d/%m/%Y %I:%M %p')
        end_time = timezone.datetime.strptime(request.POST.get('end_time'), '%d/%m/%Y %I:%M %p')
        print(request.user, start_time, end_time)
        try:
            SlotService().create_slot(request.user, start_time, end_time)
            messages.success(request, "Hurrah!!! Slot added successfully")
        except Exception as e:
            logger.exception("exception while creating slot")
            messages.error(request, "Hiss!!! Found Overlapping slot")
        return redirect("/slots/create")


@login_required
def manage_slot(request):
    if request.method == "GET":
        slot_date = request.GET.get("slot_date")
        if not slot_date:
            slot_date = timezone.now().date()
        else:
            slot_date = timezone.datetime.strptime(slot_date, '%d/%m/%Y').date()
        return render(request, "manage_slot.html", {"page": 'manage_slot', "slots": SlotService().get_all_slot_list(request.user, slot_date)})
    elif request.method == "POST":
        slot_id = request.POST["slot_id"]
        if slot_id.isnumeric():
            try:
                SlotService().del_slot(request.user, slot_id)
                messages.success(request, "Hurrah!!! Slot deleted successfully")
            except Exception:
                logger.exception("exception while deleting slot")
                messages.error(request, "Hiss!!! Slot is being used")
        else:
            messages.error(request, "Hiss!!! Please select slot first")
        return redirect(f"/slots/manage?slot_date={request.POST['slot_date']}")
