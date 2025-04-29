from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.CharField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'contact', 'role', 'image', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.method == 'POST':
            self.fields['full_name'].required = True
            self.fields['contact'].required = True
            self.fields['email'].required = True
            self.fields['image'].required = False

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
