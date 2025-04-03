from rest_framework import serializers
from .models import Category, Auction, Bid
from django.utils import timezone
from drf_spectacular.utils import extend_schema_field

# Auction serializers
class AuctionListCreateSerializer(serializers.ModelSerializer):
    # Cambiar formato:
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    # Campo dinámico
    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField()) 
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")

    isOpen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Auction
        fields = '__all__'

    @extend_schema_field(serializers.BooleanField()) 
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()


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

    class Meta:
        model = Bid
        fields = "__all__"

class BidDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"