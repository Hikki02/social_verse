from django.db.models import Count
from services.base.service import BaseService
from services.country_layer.country_layer import CountryLayerService
from ..models import Country


class ListCountryService(BaseService):
    """
    Service for listing countries.
    """
    model = Country

    def get_countries_with_posts(self):
        """
        Возвращает список стран, у которых есть хотя бы один пост.
        """
        return self.model.objects.annotate(post_count=Count('post')).filter(post_count__gt=0)


class RetrieveCountryService(BaseService):
    """
    Service for retrieving a country.
    """
    model = Country

    @classmethod
    def get_by_id(cls, object_id: int):
        """Переопределяем метод получения страны по ID, чтобы включить дополнительные данные.

        Args:
            object_id: The ID of the model instance to retrieve.

        Returns:
            dict: Словарь с данными о стране и дополнительной информацией.

        Raises:
            NotFound: Если страна не найдена.
        """
        country_layer_service = CountryLayerService
        country = super().get_by_id(object_id)
        country_data = country_layer_service.get_country_by_name(country.name)
        return {
            'country': country,
            'country_data': country_data
        }


class CountryService:
    def __init__(self,
                 list_service: ListCountryService,
                 retrieve_service: RetrieveCountryService,
                 ):
        self.list_service = list_service
        self.retrieve_service = retrieve_service

    def list_countries(self):
        return self.list_service.get_all()

    def list_countries_with_posts(self):
        """
        Возвращает список стран, у которых есть хотя бы один пост.
        """
        return self.list_service.get_countries_with_posts()

    def retrieve_country(self, country_id: int):
        return self.retrieve_service.get_by_id(country_id)
