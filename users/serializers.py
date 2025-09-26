from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra fields to the response
        data.update({
            "user_username":self.user.username,
            "user_id": self.user.id,
            "is_manager": self.user.is_staff,  # manager flag
        })
        return data

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "is_staff","dob"] 

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            dob=validated_data.get("dob"),
            is_staff=validated_data.get("is_staff", False),
            password=validated_data["password"],
        )
        return user
    
class UserListSerializer(serializers.ModelSerializer):
    identifier = serializers.IntegerField(source="id")
    displayName = serializers.CharField(source="username")
    birthYear = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["identifier", "displayName", "birthYear"] #Parameters required by SETU API

    def get_birthYear(self, obj):
        return obj.dob.year if obj.dob else None
