from django.contrib.auth.mixins import UserPassesTestMixin


class UserOwnsEventMixin(UserPassesTestMixin):
    
    def test_func(self):
        event_obj = self.get_object()
        return event_obj.created_by == self.request.user
