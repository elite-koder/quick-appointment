from django.utils import timezone

from slots.models import Slot


class SlotService:
    def get_free_slot_list(self, owner, appointment_date):
        return Slot.get_free_slot_list_guest(owner, appointment_date)

    def get_all_slot_list(self, owner, slot_date):
        return Slot.get_all_slot_list(owner, slot_date)

    def create_slot(self, owner, start_time, end_time):
        Slot.create_slot(owner, start_time, end_time)

    def del_slot(self, owner, slot_id):
        Slot.delete_slot(owner, slot_id)
