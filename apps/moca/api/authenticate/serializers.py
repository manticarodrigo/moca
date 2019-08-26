from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'date_of_birth', 'type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(list(validated_data))
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
            date_of_birth=validated_data['date_of_birth'],
            type=validated_data['type']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")