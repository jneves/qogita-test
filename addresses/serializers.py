from i18naddress import InvalidAddress, normalize_address
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from addresses.models import Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = [
            "url",
            "id",
            "country_code",
            "country_area",
            "city",
            "city_area",
            "street_address",
            "postal_code",
            "sorting_code",
            "owner",
        ]
        extra_kwargs = {
            "country_code": {"required": False},
            "country_area": {"required": False},
            "city": {"required": False},
            "city_area": {"required": False},
            "street_address": {"required": False},
            "postal_code": {"required": False},
            "sorting_code": {"required": False},
        }
        
    def validate(self, data):
        try:
            normalized_address = normalize_address(data)
        except InvalidAddress as e:
            error_messages = [f"{k}: {v}" for k, v in e.errors.items()]
            error_message = "; ".join(error_messages)
            raise serializers.ValidationError(
                f"Address failed to validate: {error_message}."
            )

        return normalized_address
