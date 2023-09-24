from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from slots.models import Slot
from users.models import User


class AppointmentStatus(models.TextChoices):
    SCHEDULED = "SCHEDULED"
    SHOWED_UP = "SHOWED_UP"
    NOT_SHOWED_UP = "NOT_SHOWED_UP"
    CANCELLED = "CANCELLED"
    DELETED = "DELETED"


# Create your models here.
class Appointment(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.DO_NOTHING, related_name="appointments")
    booked_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="appointments")
    status = models.CharField(max_length=50, default=AppointmentStatus.SCHEDULED, choices=AppointmentStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def create_appointment(cls, slot_id, booked_by):
        with transaction.atomic():
            slot = Slot.objects.get(id=slot_id, free_capacity__gt=0)
            cls.objects.create(slot_id=slot_id, booked_by=booked_by)
            Slot.objects.filter(id=slot.id).update(free_capacity=F("free_capacity")-1)

    @classmethod
    def delete_appointment(cls, appointment_id, booked_by):
        with transaction.atomic():
            slot = cls.objects.get(id=appointment_id).slot
            cls.objects.filter(id=appointment_id, booked_by=booked_by).delete()
            Slot.objects.filter(id=slot.id).update(free_capacity=F("free_capacity")+1)

    @classmethod
    def get_guest_upcoming_appointments(cls, booked_by):
        fields = ["id", "slot__start_time", "slot__end_time"]
        data = cls.objects.filter(booked_by=booked_by, slot__start_time__gt=timezone.now()).select_related("slots").order_by("slot__start_time").values(*fields)
        for dd in data:
            start_time = dd.pop("slot__start_time").strftime("%d/%m/%Y %I:%M %p")
            end_time = dd.pop("slot__end_time").strftime("%d/%m/%Y %I:%M %p")
            dd["time"] = f'{start_time} - {end_time}'
        return data

    @classmethod
    def get_host_upcoming_appointments(cls, owner):
        fields = ["id", "slot_id", "slot__start_time", "sloat__end_time", "status"]
        return cls.objects.filter(slot__owner=owner, slot__start_time__gt=timezone.now()).select_related("slots").values(*fields)
