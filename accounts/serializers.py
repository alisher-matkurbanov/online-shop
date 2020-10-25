from typing import Dict

from rest_framework import serializers
from accounts.models import USERNAME_LENGTH, PASSWORD_LENGTH, Account

MAX_LENGTH_ERROR = '{field} max length must be {number} characters'
REQUIRED_ERROR = '{field} is required'


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=USERNAME_LENGTH, error_messages={
        'required': REQUIRED_ERROR.format(field='username'),
        'max_length': MAX_LENGTH_ERROR.format(field='username', number=USERNAME_LENGTH),
    })
    password = serializers.CharField(max_length=PASSWORD_LENGTH, error_messages={
        'required': REQUIRED_ERROR.format(field='password'),
        'max_length': MAX_LENGTH_ERROR.format(field='password', number=PASSWORD_LENGTH),
    })
    
    class Meta:
        model = Account
        fields = ['username', 'password']
