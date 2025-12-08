from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Уведомление пользователя
    """
    NOTIFICATION_TYPES = (
        ('response', 'Новый отклик'),
        ('response_accepted', 'Отклик принят'),
        ('response_rejected', 'Отклик отклонен'),
        ('review', 'Новый отзыв'),
        ('order_update', 'Обновление заказа'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Пользователь'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name='Тип уведомления'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    message = models.TextField(
        verbose_name='Сообщение'
    )
    related_object_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='ID связанного объекта'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.title} для {self.user.username}"
