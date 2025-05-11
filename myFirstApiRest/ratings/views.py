from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Rating
from .serializers import RatingListCreateSerializer, RatingDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RatingListCreate(generics.ListCreateAPIView):
    serializer_class = RatingListCreateSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Rating.objects.all()


# Ver, actualizar, eliminar auction concreta
class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingDetailSerializer
    
    def get_queryset(self):
        auction_id = self.kwargs['pk']
        return Rating.objects.filter(auction=auction_id)

    def perform_update(self, serializer):
        serializer.save()