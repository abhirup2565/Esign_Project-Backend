from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['user_id'] = user.id
        token['is_manager'] = user.groups.filter(name='Managers').exists()
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra fields in login response
        data['user_id'] = self.user.id
        data['is_manager'] = self.user.groups.filter(name='Managers').exists()
        return data