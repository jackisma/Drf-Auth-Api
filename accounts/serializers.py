from os import link
from xml.dom import ValidationErr
from rest_framework import serializers
from .models import User
from django.utils.encoding import force_bytes , smart_str , DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


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






# First User Password Reset Serializer 
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("user id encoded, and it's: ",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token: ',token)
            link = "http://localhost:3000/Api/resetpassword/"+uid+'/'+token
            print('password reset link: ',link)  
            return attrs
        else:
            raise ValidationErr('User Doesn\'t exist! ')




 

# User Reset Password Serializer 
class ResetPasswordSerializer(serializers.Serializer): 
    password = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['password','password2']
    
    # Check the Validation Between User's New Password and Confirm New Password  
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError('Your Password and confirm Password Doesn\'t Match!')
        # decoding the uid and find the specific user
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError('Token is Expired or Invalid')
        user.set_password(password)
        user.save()
        return attrs
