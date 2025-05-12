from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from auctions.models import Auction, Bid, Comment, Rating
from datetime import date
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'birth_date', 'municipality',
            'locality', 'password', 'first_name', 'last_name'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        user = self.instance
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
    
    def validate_birth_date(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("You must be at least 18 years old to register.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

class AuctionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Auction
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    auction_id = serializers.SerializerMethodField()
    auction_title = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ['id', 'price', 'creation_date', 'auction_id', 'auction_title']

    def get_auction_id(self, obj):
        return obj.auction.id

    def get_auction_title(self, obj):
        return obj.auction.title

class CommentSerializer(serializers.ModelSerializer):
    auction_id = serializers.SerializerMethodField()
    auction_title = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'title', 'text', 'created_at', 'auction_id', "auction_title"]

    def get_auction_id(self, obj):
        return obj.auction.id

    def get_auction_title(self, obj):
        return obj.auction.title

class RatingSerializer(serializers.ModelSerializer):
    auction_id = serializers.SerializerMethodField()
    auction_title = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['id', 'value', 'user', 'auction_id', 'auction_title']

    def get_auction_id(self, obj):
        return obj.auction.id

    def get_auction_title(self, obj):
        return obj.auction.title