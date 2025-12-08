from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
def update_executor_rating_on_save(sender, instance, **kwargs):
    """
    Обновляет рейтинг исполнителя при создании/обновлении отзыва
    """
    if hasattr(instance.executor, 'executor_profile'):
        instance.executor.executor_profile.calculate_average_rating()


@receiver(post_delete, sender=Review)
def update_executor_rating_on_delete(sender, instance, **kwargs):
    """
    Обновляет рейтинг исполнителя при удалении отзыва
    """
    if hasattr(instance.executor, 'executor_profile'):
        instance.executor.executor_profile.calculate_average_rating()
