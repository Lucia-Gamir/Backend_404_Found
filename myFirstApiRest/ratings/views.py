from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Rating
from .serializers import RatingListCreateSerializer, RatingDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RatingListCreate(generics.ListCreateAPIView):
    serializer_class = RatingListCreateSerializer
    queryset = Rating.objects.all()


# Ver, actualizar, eliminar auction concreta
class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingDetailSerializer
    queryset = Rating.objects.all()
    #permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()