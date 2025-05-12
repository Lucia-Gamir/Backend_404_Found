from django.urls import path
from .views import UserRegisterView, UserListView, UserRetrieveUpdateDestroyView, UserProfileView, LogoutView, LoginView, MyAuctionsView, MyBidsView, MyCommentsView, MyRatingsView

app_name="users"
urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('log-out/', LogoutView.as_view(), name='log-out'),
    path('myAuctions/', MyAuctionsView.as_view(), name='my-auctions'),
    path('myBids/', MyBidsView.as_view(), name='my-bids'),
    path('myComments/', MyCommentsView.as_view(), name='my-comments'),
    path('myRatings/', MyRatingsView.as_view(), name='my-ratings'),
]
