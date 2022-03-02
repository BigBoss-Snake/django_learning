from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from .serializers import RegistrationSerializer, LoginSerializer
from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    auth_response = openapi.Response('пользователь создан')

    @swagger_auto_schema(
        operation_description="Метод создания пользователя в БД.",
        request_body=RegistrationSerializer,
        responses={201: auth_response}
    )
    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        search_id = User.objects.get(email=user.get('email'))
        user_token = search_id.token()
        uid = urlsafe_base64_encode(force_bytes(search_id.id))
        message = render_to_string('acc_active_email.html', {
            'user': user.get('email'),
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(search_id.id)),
            'token': search_id.token(),
            })

        to_email = user.get('email', None)
        email = EmailMessage(
                mail_subject, message, to=[to_email]
        )
        email.send()

        return Response(f'{current_site.domain}/users/activate/{uid}/{user_token}', status=status.HTTP_201_CREATED)  # noqa: E501


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user.token() == token:
        user.is_active = True
        user.save()

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  # noqa: E501
    else:
        return HttpResponse('Activation link is invalid!')


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    auth_response = openapi.Response('пользователь создан')

    @swagger_auto_schema(
        operation_description="Метод создания пользователя в БД.",
        request_body=LoginSerializer,
        responses={200: auth_response}
    )
    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
