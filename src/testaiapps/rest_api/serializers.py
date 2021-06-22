from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import TestCase, TestSuiteItem, TestSuites


class UserSerializer(serializers.ModelSerializer):
    """
    Using In built DRF Sericalaizer to get user info.
    """

    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    """ 
    Overriding create method to include Token for token Authentication
    Authentication used: django rest framework TokenAuthentication
    
    """
    def create(self, validate_data):
        user = User.objects.create_user(**validate_data)
        Token.objects.create(user=user)
        return user


class TestCaseSerializer(serializers.ModelSerializer):
    """ Serializer fo the Test Case """

    class Meta:
        model = TestCase
        fields = ('id', 'title', 'slug', 'description')


class TestSuiteItemSerializer(serializers.ModelSerializer):
    """Serializer for the Test Suite Item model."""
    # testcase = TestCaseSerializer(read_only=True)

    class Meta:
        model = TestSuiteItem
        fields = '__all__'


class TestSuitesSerializer(serializers.ModelSerializer):
    """ Serializer fo the test suite single test case """

    class Meta:
        model = TestSuites
        fields = '__all__'
