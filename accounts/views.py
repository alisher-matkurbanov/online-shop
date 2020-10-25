from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer


class RegisterView(ObtainAuthToken):
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        if not serializer.is_valid():
            # todo convert errors to strings
            # errors = {
            #     key: [item for item in value]
            #     for key, value in serializer.errors.items()
            # }
            errors = serializer.errors
            return Response(
                data={'success': False, 'errors': errors},
                status=400,
            )
        username = serializer.validated_data['username']
        if User.objects.filter(username=username).exists():
            return Response(
                data={'success': False, 'errors': {'general': 'User already exists'}},
                status=400,
            )
        user = User.objects.create(**serializer.validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            data={'success': True, 'token': token.key, },
            status=201,
        )
