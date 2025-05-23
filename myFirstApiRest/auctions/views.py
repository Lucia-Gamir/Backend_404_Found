from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import Category, Auction, Bid, Comment, Rating
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidListCreateSerializer, BidDetailSerializer, CommentSerializer, RatingListCreateSerializer, RatingDetailSerializer
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.utils import timezone
from datetime import datetime


# Ver auctions
class AuctionListCreate(generics.ListCreateAPIView):
    serializer_class = AuctionListCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    # Filtrar en funcion de los query params
    def get_queryset(self):
        queryset = Auction.objects.all()
        texto = self.request.query_params.get("texto", None)
        categoria = self.request.query_params.get("categoria", None)
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
    
    def perform_create(self, serializer):
        serializer.save(auctioneer=self.request.user)

class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

    def perform_update(self, serializer):
        serializer.save()

# Ver categorías
class CategoryListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


# Ver todas las bid de una subasta
class BidListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BidListCreateSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"]
        return Bid.objects.filter(auction_id=auction_id) 
    
    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        auction = get_object_or_404(Auction, id=auction_id)
        serializer.save(auction=auction, bidder=self.request.user)

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        auction_id = self.kwargs["auction_id"] 
        return Bid.objects.filter(auction_id=auction_id) 

    def perform_create(self, serializer):
        auction_id = self.kwargs["auction_id"]
        serializer.save(auction_id=auction_id) 

class BidCreateView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidListCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)
 

# Para mis auctions
class UserAuctionListView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        
        user_auctions = Auction.objects.filter(auctioneer=request.user)

        texto = self.request.query_params.get("texto", None)
        categoria = self.request.query_params.get("categoria", None)
        precio_min = self.request.query_params.get("precioMin", None)
        precio_max = self.request.query_params.get("precioMax", None)
        rating_min = self.request.query_params.get("ratingMin", None)
        rating_max = self.request.query_params.get("ratingMax", None)
        stock_min = self.request.query_params.get("stockMin", None)
        stock_max = self.request.query_params.get("stockMax", None)
        brand = self.request.query_params.get("brand", None)

        if texto:
            user_auctions = user_auctions.filter(Q(title__icontains=texto) | Q(description__icontains=texto))

        if categoria:
            user_auctions = user_auctions.filter(category__name__iexact=categoria)

        if precio_min is not None and precio_max is not None:
            user_auctions = user_auctions.filter(price__gte=precio_min, price__lte=precio_max)

        if rating_min is not None and rating_max is not None:
            user_auctions = user_auctions.filter(rating__gte=rating_min, rating__lte=rating_max)

        if stock_min is not None and stock_max is not None:
            user_auctions = user_auctions.filter(stock__gte=stock_min, stock__lte=stock_max)

        if brand:
            user_auctions = user_auctions.filter(brand__iexact=brand)

        serializer = AuctionListCreateSerializer(user_auctions, many=True, context={"request": request})

        return Response(serializer.data)
    

# Comentarios
class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise NotFound("Subasta no encontrada.")
        return Comment.objects.filter(auction=auction).order_by('-created_at')

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise NotFound("Subasta no encontrada.")
        serializer.save(user=self.request.user, auction=auction)

class CommentsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionDenied("No puedes editar este comentario.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("No puedes borrar este comentario.")
        instance.delete()


# Ratings
class RatingListCreate(generics.ListCreateAPIView):
    serializer_class = RatingListCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        auction_id = self.kwargs['auction_id']
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise NotFound("Subasta no encontrada.")
        return Rating.objects.filter(auction=auction)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            raise NotFound("Subasta no encontrada.")
        serializer.save(user=self.request.user, auction=auction)

class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().user:
            raise PermissionDenied("No puedes editar esta valoración.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user:
            raise PermissionDenied("No puedes borrar esta valoración.")
        instance.delete()


# Calendario
class CalendarView(APIView):
    def get(self, request, *args, **kwargs):
        auctions = Auction.objects.all()
        
        serializer = AuctionDetailSerializer(auctions, many=True)

        calendar_data = []
        for auction in serializer.data:

            calendar_data.append({
                'title': auction['title'],
                'start': auction['creation_date'],
                'end': auction['closing_date'],
                'description': auction['description'],
                'id': auction['id'],
            })

        return Response(calendar_data, status=status.HTTP_200_OK)