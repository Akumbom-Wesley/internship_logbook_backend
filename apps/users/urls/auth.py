from django.urls import path
from apps.users.views.auth import RegisterView, LoginView, CurrentUserView, RoleSelectionView, VerifySupervisorView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('select-role/', RoleSelectionView.as_view(), name='select_role'),
    path('verify-supervisor/<int:supervisor_id>/', VerifySupervisorView.as_view(), name='verify-supervisor'),
]