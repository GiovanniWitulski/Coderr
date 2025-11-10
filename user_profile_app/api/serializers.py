"""
Serializers for the 'user_profile_app'.
"""

from rest_framework import serializers
from ..models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    """
    A simple helper serializer for the built-in User model.
    Used for nesting User details within other serializers.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializes the UserProfile model.
    """

    # --- Fields sourced from the related User model ---
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
        """
        Overrides the default update method to handle nested User fields. 
        """
        
        # extract and remove User-related data
        user_data = validated_data.pop('user', {})

        # update User fields
        user = instance.user
        for attr, value in user_data.items():
             setattr(user, attr, value)
        user.save()

        # update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        return instance

    def to_representation(self, instance):
        """
        Overrides the output format.
        
        - Ensures a flat structure by pulling User data.
        - Replaces all `None` (null) values with empty strings (`''`)
          to prevent frontend crashes.
        """

        representation = super().to_representation(instance)
        user_representation = UserSerializer(instance.user).data

        # Manually flatten User data into the response
        representation['username'] = user_representation.get('username')
        representation['first_name'] = user_representation.get('first_name') or ''
        representation['last_name'] = user_representation.get('last_name') or ''
        representation['email'] = user_representation.get('email')

        # List of fields to check for `None`
        fields_to_format = ['location', 'tel', 'description', 'working_hours', 'file']
        for field in fields_to_format:
            if representation.get(field) is None:
                representation[field] = ''
        return representation

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes data for new user registration.
    Validates that passwords match and email is unique.
    """

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
        """
        Custom validation to check for password mismatch and existing email.
        """

        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError({"password": "passwords do not match."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "This email address is already in use."})

        return attrs

    def create(self, validated_data):
        """
        Overrides default create to handle the 'type' and 'repeated_password'
        fields and create both User and UserProfile.
        """

        # Pop custom fields that are not part of the User model
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')

        # Use create_user() to correctly hash the password
        user = User.objects.create_user(**validated_data)

        # Create the associated UserProfile
        UserProfile.objects.create(user=user, type=user_type)
        
        return user
    

class LoginSerializer(serializers.Serializer):
    """
    Serializer for the Login endpoint.
    This is not a ModelSerializer. It just validates the presence of
    username and password and uses Django's `authenticate` method.
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Validates the user's credentials.
        """

        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Authenticate the user
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                # Authentication failed
                raise serializers.ValidationError("Invalid login credentials.", code='authorization')
        else:
            # Missing fields
            raise serializers.ValidationError("Username and password are required.", code='authorization')
        # Pass the user object to the view if validation succeeds
        data['user'] = user
        return data