from django.urls import path
from ..views.users import UserListView, UserDeleteView ,UserUpdateView, UserDetailView

urlpatterns = [
    path('list', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/update/', UserUpdateView.as_view(), name='user-self-update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]