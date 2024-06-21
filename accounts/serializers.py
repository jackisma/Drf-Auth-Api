from rest_framework import serializers
from .models import User

# User Registeration Serializer 
class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name','email','password','password2','remember_me']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    # Validate The Data We Received From Client
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Your password and confirm password are not match')
        return attrs 
    
    # User Creation Operation Function 
    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


    
# User Login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User 
        fields = ['email','password']


# User Profile Serializer 
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['email','password']
        


# User Change Password Serializer 
class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']
    
    # Check the Validation Between User's Password and Confirm Password  
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Your Password and confirm Password Doesn\'t Match!')
        user.set_password(password)
        user.save()
        return attrs
        