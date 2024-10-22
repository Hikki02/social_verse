from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from rest_framework import serializers, status
from typing import Type, Dict, Any


class BaseService:
    """Base service class to handle common CRUD operations.

    Attributes:
        model: A Django model class that this service will operate on.
    """

    model: Type[models.Model] = None

    @classmethod
    def create(cls, **kwargs):
        """Creates a new instance of the model.

        Args:
            **kwargs: Field names and values for the new instance.

        Returns:
            The created model instance.

        Raises:
            ValidationError: If the instance fails validation.
        """
        try:
            obj = cls.model(**kwargs)
            obj.save()
        except ValidationError as e:
            raise ValidationError(str(e))
        return obj

    @classmethod
    def get_all(cls) -> models.QuerySet:
        """Retrieves all instances of the model.

        Returns:
            QuerySet: A queryset containing all model instances.
        """
        return cls.model.objects.all()

    @classmethod
    def get_by_id(cls, object_id: int):
        """Retrieves a single instance of the model by ID.

        Args:
            object_id: The ID of the model instance to retrieve.

        Returns:
            The model instance.

        Raises:
            ValidationError: If the instance does not exist.
        """
        try:
            objects = cls.model.objects.get(pk=object_id)
        except cls.model.DoesNotExist:
            raise serializers.ValidationError(f"{cls.model.__name__} does not exist.")
        return objects

    @classmethod
    def update(cls, object_id: int, **kwargs: Dict[str, Any]):
        """Updates an existing instance of the model.

        Args:
            object_id: The ID of the model instance to update.
            **kwargs: Field names and values to update.

        Returns:
            The updated model instance.
        """
        obj = cls.get_by_id(object_id)
        for attr, value in kwargs.items():
            setattr(obj, attr, value)
        obj.save()
        return obj

    @classmethod
    def delete(cls, object_id: int) -> JsonResponse:
        """Deletes an existing instance of the model.

        Args:
            object_id: The ID of the model instance to delete.

        Returns:
            JsonResponse: A response indicating success.
        """
        obj = cls.get_by_id(object_id)
        obj.delete()
        return JsonResponse({"message": f"{cls.model.__name__} deleted successfully."}, status=status.HTTP_200_OK)

    @classmethod
    def filter(cls, parameters: Dict[str, Any], prefetch_: list, select_: list) -> models.QuerySet:
        """Filters model instances based on given parameters.

        Args:
            parameters: A dictionary of filter parameters.
            prefetch_: A list of related fields to prefetch.
            select_: A list of related fields to select.

        Returns:
            QuerySet: A queryset containing filtered model instances.
        """
        return cls.model.objects.filter(**parameters).prefetch_related(*prefetch_).select_related(*select_)
