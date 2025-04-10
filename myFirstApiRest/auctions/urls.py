from django.urls import path
from .views import AuctionListCreate, AuctionRetrieveUpdateDestroy, CategoryListCreate, CategoryRetrieveUpdateDestroy, BidListCreate, BidRetrieveUpdateDestroy, UserAuctionListView

app_name="auctions"

urlpatterns = [
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('<int:auction_id>/bids/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bids/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail-update-delete'),
    path('users/', UserAuctionListView.as_view(), name='action-from-users'), 
]