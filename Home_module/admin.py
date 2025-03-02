from django.contrib import admin
from Home_module.models import Doctors, TimeSlot, User, Degree, Specialty


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone")

class DegreeAdmin(admin.ModelAdmin):
    class Meta:
        model = Specialty

class DoctorsAdmin(admin.ModelAdmin):
    class Meta:
        model = Doctors
        exclude = ['speciality',]

class TimeSlotAdmin(admin.ModelAdmin):
    class Meta:
        model = TimeSlot
        fields = ("doctor", "start_time", "end_time", "interval_minutes")



admin.site.register(Doctors, DoctorsAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Specialty, DegreeAdmin)