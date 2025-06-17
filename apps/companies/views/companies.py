from rest_framework import generics, permissions
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer

# Custom permission for company admins to update
class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only company admins related to this company can update
        if hasattr(request.user, 'company_admin'):
            return request.user.company_admin.company == obj
        return False

# Create – Admins only
class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# List – Authenticated users
class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

# Retrieve – Authenticated users
class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

# Update – Company Admins only (for their own company)
class CompanyUpdateView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyAdminOrReadOnly]

# Delete – Admins only
class CompanyDeleteView(generics.DestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
