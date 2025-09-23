from rest_framework import serializers
from .models import Signature, Signer
from django.contrib.auth import get_user_model
User = get_user_model()

class SignerSerializer(serializers.ModelSerializer):
    # Include username from the related user
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = Signer
        fields = ['user_id', 'username', 'status',"signer_url"]  # Add more fields if needed

class SignatureSerializer(serializers.ModelSerializer):
    signers = SignerSerializer(many=True, read_only=True)

    class Meta:
        model = Signature
        fields = ['document_id', 'signature_id', 'status', 'signers']
