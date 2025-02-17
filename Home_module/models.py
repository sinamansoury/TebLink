from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import timedelta, datetime

from Main_module.models import Speciality, Consultant


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=11, unique=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        return self.username


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Doctors(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    speciality_name = models.CharField(max_length=100, verbose_name='تخصص پزشک')
    consultant = models.ForeignKey(Consultant,on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='دسته بندی'
    )
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تخصص")
    number = models.IntegerField(verbose_name='شماره نظام پزشکی', unique=True)
    address = models.CharField(max_length=100, verbose_name='آدرس')
    phone = models.CharField(max_length=11, verbose_name='شماره موبایل', null=True, blank=True)
    main_phone = models.CharField(max_length=11, verbose_name='شماره مطب')
    photo = models.ImageField(upload_to="doctors")

    def save(self,*args, **kwargs):
        if self.speciality_name:
            speciality_obj, created = Speciality.objects.get_or_create(name=self.speciality_name)
            self.speciality = speciality_obj  # مقدار `speciality` را ذخیره کن

            if created:
                speciality_obj.count = 1
            else:
                speciality_obj.count += 1
            speciality_obj.save()

        if self.consultant:  # بررسی اگر دسته‌بندی مقدار داشته باشد
            consultant_obj, created = Consultant.objects.get_or_create(consultant=self.consultant.consultant)
            self.consultant = consultant_obj

            if created:
             consultant_obj.count = 1
            else:
                consultant_obj.count += 1
            consultant_obj.save()

        super().save(*args, **kwargs)  # ذخیره نهایی

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دکتر'
        verbose_name_plural = 'دکترها'


class DayOfWeek(models.Model):
    name = models.CharField(max_length=20, choices=[
        ('saturday', 'شنبه'),
        ('sunday', 'یکشنبه'),
        ('monday', 'دوشنبه'),
        ('tuesday', 'سه‌شنبه'),
        ('wednesday', 'چهارشنبه'),
        ('thursday', 'پنج‌شنبه'),
        ('friday', 'جمعه'),
    ])

    def __str__(self):
        return self.get_name_display()

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_minutes = models.IntegerField(default=30, choices=[(15, '15 دقیقه'), (30, '30 دقیقه'),
                                                                (45, '45 دقیقه'), (60, '1 ساعت')])
    days = models.ManyToManyField(DayOfWeek)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_appointment_slots()

    def generate_appointment_slots(self):
        start_time = datetime.strptime(str(self.start_time), "%H:%M:%S").time()
        end_time = datetime.strptime(str(self.end_time), "%H:%M:%S").time()

        current_time = start_time
        while current_time < end_time:
            AppointmentSlot.objects.create(
                doctor=self.doctor,
                time_slot=self,
                time=current_time
            )
            current_time = (datetime.combine(datetime.today(), current_time) +
                            timedelta(minutes=self.interval_minutes)).time()

    def __str__(self):
        return f"زمان‌بندی {self.doctor} از {self.start_time} تا {self.end_time} با بازه {self.interval_minutes} دقیقه"

    class Meta:
        verbose_name = 'تایم ویزیت'
        verbose_name_plural = 'تایم های ویزیت'


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('reserved', 'رزرو شده'), ('empty', 'خالی')], default='empty')

    def __str__(self):
        return f"{self.time} - {self.doctor} ({self.status})"
