from rest_framework import serializers
from .models import User, Category, Pet, AdoptionApplication

# Serializer for User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'mobile_no', 'address', 'is_admin', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

# Serializer for Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializer for Pet
class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

# Serializer for AdoptionApplication
class AdoptionApplicationSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = AdoptionApplication
        
        read_only_fields = ['user']
        fields = '__all__'
