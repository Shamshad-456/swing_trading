from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update an existing user with the validated data."""
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)  # Hash the password if updated
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
