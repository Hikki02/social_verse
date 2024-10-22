from django.db import models

from services.base.models import TimeStampModel


class Country(TimeStampModel):
    """
    Модель Country представляет собой список стран.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name
