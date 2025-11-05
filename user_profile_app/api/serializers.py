from rest_framework import serializers
from ..models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True) 
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = UserProfile
        fields = [
            'id',             
            'user',           
            'username',       
            'first_name',     
            'last_name',      
            'email',          
            'type',           
            'file',           
            'location',       
            'tel',            
            'description',    
            'working_hours',  
            'created_at',
        ]
        read_only_fields = ['user', 'type', 'created_at'] 

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {}) 
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = UserSerializer(instance.user).data
        representation['username'] = user_representation.get('username')
        representation['first_name'] = user_representation.get('first_name') or ''
        representation['last_name'] = user_representation.get('last_name') or ''
        representation['email'] = user_representation.get('email')

        fields_to_format = ['location', 'tel', 'description', 'working_hours', 'file']
        for field in fields_to_format:
            if representation.get(field) is None:
                representation[field] = ''
        return representation

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    type = serializers.ChoiceField(choices=UserProfile.UserType.choices, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({"password": "passwords do not match."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email address is already in use."})

        return attrs

    def create(self, validated_data):
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')

        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, type=user_type)
        
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid login credentials.", code='authorization')
        else:
            raise serializers.ValidationError("Username and password are required.", code='authorization')

        data['user'] = user
        return data