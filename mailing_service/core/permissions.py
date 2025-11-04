from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_manager

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для выполнения этого действия")


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_manager or self.request.user.groups.filter(name='Менеджеры').exists()

    def handle_no_permission(self):
        raise PermissionDenied("Требуются права менеджера")


class CanViewAllMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_manager or self.request.user.groups.filter(name='Менеджеры').exists():
            return queryset
        return queryset.filter(owner=self.request.user)
