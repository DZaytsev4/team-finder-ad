from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerOrStaffMixin(UserPassesTestMixin):
    def test_func(self):
        project = self.get_object()
        return self.request.user.is_staff or project.owner_id == self.request.user.id

