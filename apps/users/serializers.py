from rest_framework import serializers
from .models import User, Address

class AuthorizeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    password = serializers.CharField(write_only=True, required=False)
    name = serializers.CharField(required=False)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, value):
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("User not found")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country']

class UserSerializer(serializers.ModelSerializer):
    default_shipping_address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'email', 'default_shipping_address', 'date_joined']
        read_only_fields = ['id', 'phone', 'date_joined']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('default_shipping_address', None)
        if address_data:
            address = instance.default_shipping_address
            if address:
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                address = Address.objects.create(**address_data)
                instance.default_shipping_address = address

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
