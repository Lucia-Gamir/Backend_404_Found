from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidListCreateSerializer, BidDetailSerializer
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin 
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Ver auctions
class AuctionListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AuctionListCreateSerializer

    # Filtrar en funcion de los query params
    def get_queryset(self):
        queryset = Auction.objects.all()
        texto = self.request.query_params.get("texto", None)
        categoria = self.request.query_params.get("categoría", None)
        precio_min = self.request.query_params.get("precioMin", None)
        precio_max = self.request.query_params.get("precioMax", None)
        rating_min = self.request.query_params.get("ratingMin", None)
        rating_max = self.request.query_params.get("ratingMax", None)
        stock_min = self.request.query_params.get("stockMin", None)
        stock_max = self.request.query_params.get("stockMax", None)
        brand = self.request.query_params.get("brand", None)

        if texto:
            queryset = queryset.filter(Q(title__icontains=texto) | Q(description__icontains=texto))

        if categoria:
            queryset = queryset.filter(category__name__iexact=categoria)

        if precio_min is not None and precio_max is not None:
            queryset = queryset.filter(price__gte=precio_min, price__lte=precio_max)

        if rating_min is not None and rating_max is not None:
            queryset = queryset.filter(rating__gte=rating_min, rating__lte=rating_max)

        if stock_min is not None and stock_max is not None:
            queryset = queryset.filter(stock__gte=stock_min, stock__lte=stock_max)

        if brand:
            queryset = queryset.filter(brand__iexact=brand)

        return queryset

# Ver, actualizar, eliminar auction concreta
class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer


# Ver categorías
class CategoryListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()  # BBDD ¿qué dato devuelvo?
    serializer_class = CategoryListCreateSerializer  # Llamada al serializador ¿cómo lo devuelvo?

# Ver, actualizar, eliminar categoría concreta
class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


# Ver todas las bid de una subasta
class BidListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BidListCreateSerializer

    def get_queryset(self):  # Filtrar por parametros de entrada
        auction_id = self.kwargs["auction_id"]
        return Bid.objects.filter(auction_id=auction_id) 
    
    def perform_create(self, serializer):  # Guardar la puja
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id)

# Ver, actualizar, eliminar Bid concreta
class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"] 
        return Bid.objects.filter(auction_id=auction_id) 

    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id) 

 
class UserAuctionListView(APIView): 
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs): 
        # Obtener las subastas del usuario autenticado 
        user_auctions = Auction.objects.filter(auctioneer=request.user) 
        serializer = AuctionListCreateSerializer(user_auctions, many=True) 
        return Response(serializer.data)