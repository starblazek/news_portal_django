from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import News
from .permissions import IsAuthorOrReadOnly
from .serializers import NewsSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def perform_destroy(self, instance):
        if instance != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Вы можете удалять только свой аккаунт.')
        instance.delete()

    def perform_update(self, serializer):
        if serializer.instance != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Вы можете редактировать только свой аккаунт.')
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.select_related('author').all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['author']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
