
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Literal
from urllib.parse import urljoin

import requests
from rest_framework.status import is_client_error, is_server_error

from services.request_service.exceptions import ClientNotFoundError, HubServerError

METHODS = Literal['post', 'get']


class BaseRequest(ABC):
    POST = 'post'
    GET = 'get'

    @classmethod
    @abstractmethod
    def _make_request(cls, endpoint: str, method: METHODS, **kwargs):
        raise NotImplementedError


class ServiceRequest(BaseRequest):
    BASE_URL = None

    @classmethod
    def _get_base_url(cls):
        return cls.BASE_URL

    @classmethod
    def _make_request(cls, endpoint: str, method: METHODS, **kwargs):
        url = f'{urljoin(cls._get_base_url(), endpoint)}'
        response = requests.request(
            method,
            url,
            **kwargs
        )
        if is_client_error(response.status_code):
            error_msg = None

            try:
                response_json = response.json()
                error_msg = response_json.get('message')
            except JSONDecodeError:
                response.raise_for_status()

            raise ClientNotFoundError(detail=error_msg)

        elif is_server_error(response.status_code):

            raise HubServerError()

        response.raise_for_status()

        return response
