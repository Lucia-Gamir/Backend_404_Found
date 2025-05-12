from django.urls import path
from .views import AuctionListCreate, AuctionRetrieveUpdateDestroy, CategoryListCreate, CategoryRetrieveUpdateDestroy, BidListCreate, BidRetrieveUpdateDestroy, UserAuctionListView, CommentListCreate, CommentsRetrieveUpdateDestroy, RatingListCreate, RatingRetrieveUpdateDestroy, CalendarView

app_name="auctions"

urlpatterns = [
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('<int:auction_id>/bids/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bids/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail-update-delete'),
    path('<int:auction_id>/comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('<int:auction_id>/comments/<int:pk>/', CommentsRetrieveUpdateDestroy.as_view(), name='comment-detail-update-delete'),
    path('<int:auction_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('<int:auction_id>/ratings/<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-detail'),
    path('calendar/', CalendarView.as_view(), name='calendar-view'),
]