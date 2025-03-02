from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import timedelta, datetime

from Main_module.models import Speciality


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

class Degree(models.Model):
    degree_choices = [
        ('پزشک عمومی', 'پزشک عمومی'),
        ('متخصص', 'متخصص'),
        ('phd', 'PhD'),
        ('کارشناسی ارشد', 'کارشناسی ارشد'),
        ('کارشناسی', 'کارشناسی'),
        ('دستیار تخصصی', 'دستیار تخصصی')
    ]

    name = models.CharField(
        max_length=100,
        choices=degree_choices,
        unique=True,
        verbose_name='مدرک تحصیلی'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'مدرک تحصیلی'
        verbose_name_plural = 'مدارک تحصیلی'

class Specialty(models.Model):
    name = models.CharField(max_length=100, verbose_name="رشته پزشکی")
    degrees = models.ManyToManyField(Degree, related_name='specialties', verbose_name="مدرک‌های تحصیلی")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'رشته پزشکی'
        verbose_name_plural = 'رشته‌های پزشکی'

class Doctors(models.Model):
    name = models.CharField(max_length=100,null=True, blank=True, verbose_name="نام")
    last_name = models.CharField(max_length=100,null=True, blank=True, verbose_name="نام خانوادگی")
    speciality_name = models.CharField(max_length=100,null=True, blank=True, verbose_name='تخصص پزشک')
    id_code = models.IntegerField(unique=True,null=True, blank=True, verbose_name='کد ملی')
    birthday = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ تولد')
    sex = models.CharField(choices=[('men','مرد'), ('women','زن')],null=True, blank=True,verbose_name='جنسیت',max_length=100)
    degree = models.ForeignKey(Degree,on_delete=models.CASCADE,
                               null=True, blank=True,verbose_name='مدرک تحصیلی')
    degree_name= models.CharField(max_length=100,verbose_name='نام مدرک',null=True, blank=True)
    number = models.IntegerField(verbose_name='شماره نظام پزشکی',null=True, blank=True, unique=True)
    address = models.CharField(max_length=100, verbose_name='آدرس',null=True, blank=True,)
    phone = models.CharField(max_length=11, verbose_name='شماره موبایل', null=True, blank=True)
    main_phone = models.CharField(max_length=11, verbose_name='شماره مطب',null=True, blank=True,)
    photo = models.ImageField(upload_to="doctors",null=True, blank=True,)

    def save(self, *args, **kwargs):
        is_new = self.id is None
        super().save(*args, **kwargs)

        if is_new:
            self.add_count()

    def add_count(self):
        speciality, created = Speciality.objects.get_or_create(name=self.degree_name)

        if created:
            speciality.count = 1
            speciality.save()
        else:
            speciality.count += 1
            speciality.save()

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
        is_new = self.id is None
        super().save(*args, **kwargs)

        if is_new:
            self.generate_appointment_slots()

    def generate_appointment_slots(self):
        AppointmentSlot.objects.filter(time_slot=self).delete()

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
