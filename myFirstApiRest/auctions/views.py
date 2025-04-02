from django.shortcuts import render
from rest_framework import generics
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidListCreateSerializer, BidDetailSerializer

# Ver categorías
class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()  # BBDD ¿qué dato devuelvo?
    serializer_class = CategoryListCreateSerializer  # Llamada al serializador ¿cómo lo devuelvo?

# Ver, actualizar, eliminar categoría concreta
class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

# Ver auctions
class AuctionListCreate(generics.ListCreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionListCreateSerializer

# Ver, actualizar, eliminar auction concreta
class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

# Ver todas las bid de una subasta
class BidListCreate(generics.ListCreateAPIView):
    serializer_class = BidListCreateSerializer

    def get_queryset(self):  # Lectura parámetros entrada
        auction_id = self.kwargs["auction_id"]  # Obtener el ID de la auction desde la URL
        return Bid.objects.filter(auction_id=auction_id)  # Filtrar las bids de esa auction
    
    def perform_create(self, serializer):  # Guardar la subasta
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id)

# Ver, actualizar, eliminar Bid concreta
class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"] 
        return Bid.objects.filter(auction_id=auction_id) 

    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id) 
    