from rest_framework import serializers


class CountryLayerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    topLevelDomain = serializers.ListField(
        child=serializers.CharField(max_length=10)
    )
    alpha2Code = serializers.CharField(max_length=2)
    alpha3Code = serializers.CharField(max_length=3)
    callingCodes = serializers.ListField(
        child=serializers.CharField(max_length=5)
    )
    capital = serializers.CharField(max_length=255, allow_blank=True)
    altSpellings = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    region = serializers.CharField(max_length=255)


class CountryLayerListSerializer(serializers.Serializer):
    countries = CountryLayerSerializer(many=True)
