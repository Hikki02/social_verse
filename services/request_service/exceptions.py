from rest_framework.exceptions import APIException


class ClientNotFoundError(APIException):
    status_code = 400
    default_detail = 'Неверный формат запроса!'


class HubServerError(APIException):
    status_code = 400
    default_detail = 'Ошибка сервиса ...!'
