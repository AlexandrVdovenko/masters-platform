from django.db import models
from django.conf import settings
from orders.models import Category


class PortfolioItem(models.Model):
    """
    Работа в портфолио исполнителя
    """
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio_items',
        verbose_name='Исполнитель'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='portfolio_items',
        verbose_name='Категория'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Работа в портфолио'
        verbose_name_plural = 'Работы в портфолио'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.executor.username}"


class PortfolioImage(models.Model):
    """
    Изображение работы в портфолио
    """
    portfolio_item = models.ForeignKey(
        PortfolioItem,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Работа'
    )
    image = models.ImageField(
        upload_to='portfolio/',
        verbose_name='Изображение'
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Подпись'
    )
    
    class Meta:
        verbose_name = 'Изображение портфолио'
        verbose_name_plural = 'Изображения портфолио'
    
    def __str__(self):
        return f"Изображение для {self.portfolio_item.title}"
