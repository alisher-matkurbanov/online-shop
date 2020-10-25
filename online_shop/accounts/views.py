from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from typing import Optional

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountViewSet(ModelViewSet):
    serializer_class = AccountSerializer
    renderer_classes = [JSONRenderer]
    queryset = Account.objects.all()
    
    @staticmethod
    def is_valid(serializer) -> (bool, Optional[Response]):
        if not serializer.is_valid():
            # todo convert errors to strings
            # errors = {
            #     key: [item for item in value]
            #     for key, value in serializer.errors.items()
            # }
            errors = serializer.errors
            return False, Response(
                data={'success': False, 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return True, None
    
    def list(self, request, *args, **kwargs):
        return Response(
            data={'detail': 'Not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        is_valid, response = self.is_valid(serializer)
        if not is_valid:
            return response
        username = serializer.validated_data['username']
        if Account.objects.filter(username=username).exists():
            return Response(
                data={'success': False, 'errors': {'general': 'User already exists'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = serializer.create(validated_data=serializer.validated_data)
        token = Token.objects.create(user=user)
        return Response(
            data={'success': True, 'token': token.key},
            status=status.HTTP_201_CREATED,
        )
    
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        is_valid, response = self.is_valid(serializer)
        if not is_valid:
            return response
        username = serializer.validated_data['username']
        if not Account.objects.filter(username=username).exists():
            return Response(
                data={'success': False, 'errors': {'general': 'Create user before login'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = Account.objects.get(username=username)
        token = Token.objects.get(user=user)
        return Response(
            data={'success': True, 'token': token.key},
            status=status.HTTP_200_OK,
        )
