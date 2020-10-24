from django.shortcuts import render
from rest_framework import viewsets, permissions


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('-date_joined')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
