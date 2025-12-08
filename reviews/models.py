from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from orders.models import Order


class Review(models.Model):
    """
    Отзыв о работе исполнителя
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Заказ'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        verbose_name='Заказчик'
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received',
        verbose_name='Исполнитель'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг'
    )
    comment = models.TextField(
        verbose_name='Комментарий'
    )
    executor_response = models.TextField(
        blank=True,
        verbose_name='Ответ исполнителя'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв от {self.customer.username} для {self.executor.username}"
