"""
Общие миксины для представлений
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, что пользователь является владельцем объекта
    """
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_staff


class CustomerRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, что пользователь является заказчиком
    """
    def test_func(self):
        return self.request.user.user_type == 'customer'


class ExecutorRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, что пользователь является исполнителем
    """
    def test_func(self):
        return self.request.user.user_type == 'executor'
