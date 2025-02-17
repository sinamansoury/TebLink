from django.db import models

# Create your models here.
class Consultant(models.Model):
    consultant = models.CharField(
    max_length = 100,
    choices = [
        ('پزشک عمومی', 'پزشک عمومی'),
        ('متخصص', 'متخصص'),
        ('روانشناس', 'روانشناس'),
    ],
    null = True,
    blank = True,
    verbose_name = 'دسته بندی')
    count = models.IntegerField(default=0, verbose_name='تعداد پزشکان')

    def __str__(self):
        return self.consultant

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

class Speciality(models.Model):
    name = models.CharField(max_length=100, verbose_name='تخصص')  # نام تخصص
    count = models.IntegerField(default=0, verbose_name='تعداد پزشکان')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تخصص'
        verbose_name_plural = 'تخصص‌ها'