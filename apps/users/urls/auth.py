from django.urls import path
from apps.users.views.auth import RegisterView, LoginView, CurrentUserView, RoleSelectionView, VerifySupervisorView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('select-role/', RoleSelectionView.as_view(), name='select_role'),
    path('verify-supervisor/<int:supervisor_id>/', VerifySupervisorView.as_view(), name='verify-supervisor'),
]