from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile, ExecutorProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Автоматически создает профиль при создании пользователя
    """
    if created:
        Profile.objects.create(user=instance)
        if instance.user_type == 'executor':
            ExecutorProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль при сохранении пользователя
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if instance.user_type == 'executor' and hasattr(instance, 'executor_profile'):
        instance.executor_profile.save()
