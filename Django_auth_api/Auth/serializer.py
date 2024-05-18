from rest_framework import serializers
from .models import *
from .utils import *

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AuthSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(min_length=8,style={'input_type':'password'},write_only=True)
    class Meta:
        model = MyUser
        fields = ['id','full_name','email','password','password2','tc']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password1 and  Password2 are not same") 
        return attrs
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model = MyUser
        fields = ['email','password']

class GetUserdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','full_name','email']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True}
        }
        
class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8,style={'input_type':'password'},write_only=True)
    confirmation_new_password = serializers.CharField(min_length=8,style={'input_type':'password'},write_only=True)

    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password', 'confirmation_new_password']

    def validate(self, value):
        old_password = value.get('old_password')
        new_password = value.get('new_password')
        confirmation_new_password = value.get('confirmation_new_password')
        new_pass = {"password":new_password}
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError("current password doesn't match with enter old password")
        
        if new_password == old_password:
            raise serializers.ValidationError("The new password must be different than the current one.")
        
        if new_password != confirmation_new_password:
            raise serializers.ValidationError("New password and its confirmation do not match.")
        
        user.set_password(new_password)
        user.save()
        return new_pass

class ResetPassword(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8,style={'input_type':'password'},write_only=True)
    class Meta:
        model = MyUser
        fields = ['password','password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self,value):
        try:
            password = value.get('password')
            password2 = value.get('password2')
            uuid = self.context.get('uuid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uuid))
            user = MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Your token is not valid or expired")
            elif password != password2:
                raise serializers.ValidationError("New password and its confirmation do not match.")
            elif len(password) > 8:
                raise serializers.ValidationError("Password must be at least 8 characters long.")
            else:
                user.set_password(password)
                user.save()
            return value
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Your token is not valid or expired")   
            
class SendEmailToResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=300)
    class Meta:
        model = MyUser
        fields = ['email']

    def validate(self,value):
        email = value.get('email')
        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            uuid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://127.0.0.1:8000/Auth/api/ResetPassword/"+uuid+"/"+token
            #send mail
            data = {'mail_subject':'Reset you django authentictaion api password',
                    'mail_body':f'To reset your django authentication api password, Click below link \n{link}',
                    'to':user.email}
            Util.send_mail(data)
            return value
        else:
            raise serializers.ValidationError("Email does not exist.")
