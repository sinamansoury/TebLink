from django.db import models

class Speciality(models.Model):
    name = models.CharField(max_length=100, verbose_name='تخصص')
    count = models.IntegerField(default=1, verbose_name='تعداد تخصص')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='تخصص'
        verbose_name_plural='تخصص ها'
