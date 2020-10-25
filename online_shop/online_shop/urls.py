"""online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework import routers, status
from rest_framework.response import Response

from accounts import views as accounts_views

router = routers.SimpleRouter()
router.register('', accounts_views.AccountViewSet, basename='accounts')


def handler404(*args, **kwargs):
    return JsonResponse(
        data={'detail': 'Not found.'},
        status=status.HTTP_404_NOT_FOUND
    )


handler500 = 'rest_framework.exceptions.server_error'
handler400 = 'rest_framework.exceptions.bad_request'

urlpatterns = [
    path('', handler404),
    path('api/', include(router.urls)),
]
