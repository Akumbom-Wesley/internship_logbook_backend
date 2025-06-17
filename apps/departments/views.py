from rest_framework import generics, permissions
from apps.departments.models import Department
from apps.departments.serializers import DepartmentSerializer

# List & Create – any authenticated user
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]  # Anyone logged in can list/create

# Custom permission: Admins only can update/delete
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user.is_staff

# Retrieve, Update, Delete – admin only for updates/deletes
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
