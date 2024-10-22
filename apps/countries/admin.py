from django.contrib import admin

from apps.countries.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ...
