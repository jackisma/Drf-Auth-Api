from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name','email','password','password2','remember_me']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Your password and confirm password are not match')
        return attrs 
    
    def create(self,validated_data):
        return User.objects.create(**validated_data)