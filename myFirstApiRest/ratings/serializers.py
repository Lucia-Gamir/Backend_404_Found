from rest_framework import serializers
from .models import Rating
from users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

class RatingListCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    rating_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "value", "auction", "user", "rating_username"]

    def get_rating_username(self, obj):
        return obj.user.username

    def validate(self, data):
        username = data.get('user')
        auction = data.get('auction')

        try:
            user_obj = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'user': 'Usuario no encontrado.'})


        if Rating.objects.filter(user=user_obj, auction=auction).exists():
            raise serializers.ValidationError("Este usuario ya ha valorado esta subasta.")

        data['user'] = user_obj
        return data
    

class RatingDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    rating_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "value", "auction", "user", "rating_username"]

    def get_rating_username(self, obj):
        return obj.user.username

    def validate(self, data):
        username = data.get('user')
        if username:
            try:
                user_obj = CustomUser.objects.get(username=username)
                data['user'] = user_obj
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({'user': 'Usuario no encontrado.'})
        return data

