from typing import Dict, Any

from rest_framework.exceptions import ValidationError

from services.country_layer.serializers import CountryLayerListSerializer
from services.request_service.request_service import ServiceRequest
from travel_verse.settings import COUNTRY_LAYER_BASE_URL, COUNTRY_LAYER_API_KEY


class CountryLayerService(ServiceRequest):
    BASE_URL: str = COUNTRY_LAYER_BASE_URL
    API_KEY: str = COUNTRY_LAYER_API_KEY
    HEADERS: dict = {
        'Content-Type': 'application/json',
    }

    @classmethod
    def _make_request(cls, endpoint: str, method: str, **kwargs):
        params = kwargs.get('params', {})
        params['access_key'] = cls.API_KEY
        kwargs['params'] = params
        return super()._make_request(endpoint, method, **kwargs)

    @classmethod
    def get_country_by_name(cls, country_name: str) -> Dict[str, Any]:
        """
        Найти страну по названию.
        """
        endpoint = f'name/{country_name}'
        response = cls._make_request(endpoint, cls.GET, headers=cls.HEADERS)
        country_data = response.json()

        if country_data:
            return cls._validate_country_data(country_data)
        else:
            raise ValidationError("Страна не найдена.")

    @staticmethod
    def _validate_country_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Валидация данных о стране через сериализатор.
        """
        serializer = CountryLayerListSerializer(data={'countries': data})
        if serializer.is_valid():
            return serializer.validated_data['countries']
        else:
            raise ValidationError(serializer.errors)

