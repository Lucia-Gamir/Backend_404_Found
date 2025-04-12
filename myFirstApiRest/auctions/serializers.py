from rest_framework import serializers
from .models import Category, Auction, Bid
from django.utils import timezone
from django.db import models
from drf_spectacular.utils import extend_schema_field
from datetime import timedelta

class AuctionBaseSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    def validate(self, data):
        if 'stock' in data and data['stock'] <= 0:
            raise serializers.ValidationError({"stock": "El stock debe ser un número positivo."})

        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError({"price": "El precio debe ser un número positivo."})

        if 'rating' in data:
            if data['rating'] < 1 or data['rating'] > 5:
                raise serializers.ValidationError({"rating": "La valoración debe estar entre 1 y 5."})

        creation = self.instance.creation_date if self.instance else timezone.now()
        closing = data.get('closing_date')

        if closing:
            if closing <= creation:
                raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser posterior a la de creación."})
            
            if closing <= creation + timedelta(days=15):
                raise serializers.ValidationError({"closing_date": "La fecha de cierre debe ser al menos 15 días posterior a la de creación."})

        return data

    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

class AuctionListCreateSerializer(AuctionBaseSerializer):
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return super().get_isOpen(obj)

class AuctionDetailSerializer(AuctionBaseSerializer):
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return super().get_isOpen(obj)


# Category serializers
class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']  # campos

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# Bid serializers
class BidListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "auction", "price", "creation_date", "bidder_username"]
        read_only_fields = ['bidder']

    def get_bidder_username(self, obj):
        return obj.bidder.username

    def validate(self, data):
        auction = data['auction']
        price = data['price']

        if price <= 0:
            raise serializers.ValidationError("El precio de la puja debe ser un número positivo.")
        
        max_bid = Bid.objects.filter(auction=auction).aggregate(models.Max('price'))['price__max']
        if max_bid is not None and price <= max_bid:
            raise serializers.ValidationError("La puja debe ser mayor que las existentes.")
        
        if auction.closing_date <= timezone.now():
            raise serializers.ValidationError("La subasta ya ha cerrado, no se puede pujar.")
        
        return data
    
    def create(self, validated_data):
        validated_data['bidder'] = self.context['request'].user
        return super().create(validated_data)

class BidDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    bidder_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "auction", "price", "creation_date", "bidder_username"]

    def get_bidder_username(self, obj):
        return obj.bidder.username