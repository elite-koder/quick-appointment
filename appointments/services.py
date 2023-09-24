from appointments.models import Appointment


class AppointmentService:
    def __init__(self):
        pass

    def book_appointment(self, slot_id, booking_by):
        Appointment.create_appointment(slot_id, booking_by)

    def delete_appointment(self, appointment_id, booked_by):
        Appointment.delete_appointment(appointment_id, booked_by)

    def list_guest_appointments(self, booked_by):
        return Appointment.get_guest_upcoming_appointments(booked_by)

    def list_host_appointments(self, owner):
        return Appointment.get_host_upcoming_appointments(owner)
