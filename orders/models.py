from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Category(models.Model):
    """
    Категория услуг
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Заказ от заказчика
    """
    STATUS_CHOICES = (
        ('active', 'Активен'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('deleted', 'Удален'),
    )
    
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Заказчик'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='Категория'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    budget_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Минимальный бюджет'
    )
    budget_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Максимальный бюджет'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
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
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.customer.username}"


class Response(models.Model):
    """
    Отклик исполнителя на заказ
    """
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
    )
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Заказ'
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Исполнитель'
    )
    message = models.TextField(
        verbose_name='Сообщение'
    )
    proposed_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Предложенная цена'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']
        unique_together = ['order', 'executor']
    
    def __str__(self):
        return f"Отклик от {self.executor.username} на {self.order.title}"
