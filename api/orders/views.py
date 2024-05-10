from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.models import Group, User
from .models import Article, Order, Order_Article
from rest_framework import permissions, viewsets

from api.orders.serializers import GroupSerializer, UserSerializer, ArticleSerializer, OrderSerializer, Order_ArticleSerializer 

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('name')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data
        if not data.get('creation_date'):
            data['creation_date'] = datetime.now().date()
        serializer.save(**data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('creation_date')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        if not data.get('creation_date'):
            data['creation_date'] = datetime.now().date()
        if not data.get('price'):
            data['price'] = 0
        if not data.get('tax_price'):
            data['tax_price'] = 0    
        serializer.save(**data)


class Order_ArticleViewSet(viewsets.ModelViewSet):
    queryset = Order_Article.objects.all().order_by('amount')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = Order_ArticleSerializer

