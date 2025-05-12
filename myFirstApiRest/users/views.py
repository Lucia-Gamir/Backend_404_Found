from rest_framework import status, generics 
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import CustomUser
from auctions.models import Auction, Bid
from .serializers import UserSerializer, LoginSerializer, AuctionSerializer, BidSerializer
from rest_framework import status, generics 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
 
class UserRegisterView(generics.CreateAPIView): 
    permission_classes = [AllowAny] 
    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer 
 
    def create(self, request): 
        serializer = self.get_serializer(data=request.data) 
        if serializer.is_valid(): 
            user = serializer.save() 
            refresh = RefreshToken.for_user(user) 
            return Response({ 
                'user': serializer.data, 
                'access': str(refresh.access_token), 
                'refresh': str(refresh), 
            }, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, 
status=status.HTTP_400_BAD_REQUEST) 
 
class UserListView(generics.ListAPIView): 
    permission_classes = [IsAdminUser] 
    serializer_class = UserSerializer 
    queryset = CustomUser.objects.all().order_by('id')
 
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView): 
    permission_classes = [IsAuthenticated] 
    serializer_class = UserSerializer 
    queryset = CustomUser.objects.all().order_by('id')

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'access': access_token,
                'username': user.username
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
class UserProfileView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def get(self, request): 
        serializer = UserSerializer(request.user) 
        return Response(serializer.data) 
 
    def patch(self, request): 
        serializer = UserSerializer(request.user, data=request.data, partial=True) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    def delete(self, request): 
        user = request.user 
        user.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class LogoutView(APIView): 
    permission_classes = [IsAuthenticated] 
    
    def post(self, request): 
        """Realiza el logout eliminando el RefreshToken (revocar)""" 
        try: 

            refresh_token = request.data.get('refresh', None) 
            if not refresh_token: 
                return Response({"detail": "No refresh token provided."}, 
status=status.HTTP_400_BAD_REQUEST) 
 
            token = RefreshToken(refresh_token) 
            token.blacklist()   
            return Response({"detail": "Logout successful"}, 
status=status.HTTP_205_RESET_CONTENT) 
 
        except Exception as e: 
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        
class MyAuctionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AuctionSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Auction.objects.filter(creator=self.request.user)
    
    def get_serializer_context(self):
        return {'request': self.request}

class MyBidsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)