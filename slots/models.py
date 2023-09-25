from django.db import models, transaction
from django.utils import timezone

from users.models import User


# Create your models here.
class Slot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.IntegerField()
    free_capacity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="slots")
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def create_slot(cls, owner, start_time, end_time, capacity=1):
        start_time = timezone.make_aware(start_time, timezone=timezone.get_default_timezone())
        end_time = timezone.make_aware(end_time, timezone=timezone.get_default_timezone())
        with transaction.atomic():
            if cls.objects.filter(owner_id=owner.id, start_time__lt=end_time, end_time__gt=start_time).exists():
                raise ValueError("overlapping slot found")
            cls.objects.create(start_time=start_time, end_time=end_time, capacity=capacity, free_capacity=capacity, owner=owner)

    @classmethod
    def delete_slot(cls, owner, slot_id):
        with transaction.atomic():
            slot = cls.objects.get(owner=owner, id=slot_id)
            if slot.capacity > slot.free_capacity:
                raise ValueError("being used, can't delete")
            slot.delete()

    @classmethod
    def get_free_slot_list_guest(cls, owner, date):
        if timezone.now().date() > date:
            return []
        fields = ["id", "start_time"]
        if timezone.now().date() == date:
            data = cls.objects.filter(owner=owner, start_time__gte=timezone.now(), start_time__date=date, free_capacity__gt=0).values(*fields)
        else:
            data = cls.objects.filter(owner=owner, start_time__date=date, free_capacity__gt=0).values(*fields)
        for dd in data:
            dd["time"] = dd.pop("start_time").strftime("%I:%M %p")
        return data

    @classmethod
    def get_all_slot_list(cls, owner, slot_date):
        fields = ["id", "start_time", "end_time", "capacity", "free_capacity"]
        data = cls.objects.filter(owner=owner, start_time__date=slot_date).order_by("start_time").values(*fields)
        for dd in data:
            dd["time"] = f'{dd.pop("start_time").strftime("%I:%M %p")} - {dd.pop("end_time").strftime("%I:%M %p")}, {dd.pop("capacity") - dd.pop("free_capacity")} booking(s)'
        return data

    @classmethod
    def get_free_slot_list_host(cls, owner, date):
        fields = ["id", "start_time", "end_time", "capacity", "free_capacity", "created_at"]
        return cls.objects.filter(start_time__date=date).values(*fields)
