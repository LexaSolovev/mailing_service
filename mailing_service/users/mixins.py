from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_manager

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для выполнения этого действия")