from django.urls import path
from .views import AuctionListCreate, AuctionRetrieveUpdateDestroy, CategoryListCreate, CategoryRetrieveUpdateDestroy, BidListCreate, BidRetrieveUpdateDestroy

app_name="auctions"

urlpatterns = [
    path('auctions/', AuctionListCreate.as_view(), name='auction-list-create'),
    path('auctions/<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),
    path('auctions/categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('auctions/category/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('auctions/<int:auction_id>/bids/', BidListCreate.as_view(), name='bid-list-create'),
    path('auctions/<int:auction_id>/bids/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail-update-delete'),
]