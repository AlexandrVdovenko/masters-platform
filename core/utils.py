"""
Вспомогательные функции
"""
from notifications.models import Notification


def create_notification(user, notification_type, title, message, related_object_id=None):
    """
    Создает уведомление для пользователя
    
    Args:
        user: Пользователь, которому отправляется уведомление
        notification_type: Тип уведомления
        title: Заголовок
        message: Текст сообщения
        related_object_id: ID связанного объекта (опционально)
    
    Returns:
        Notification: Созданное уведомление
    """
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_object_id=related_object_id
    )
