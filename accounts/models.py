from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя с типом аккаунта
    """
    USER_TYPE_CHOICES = (
        ('customer', 'Заказчик'),
        ('executor', 'Исполнитель'),
    )
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        verbose_name='Тип пользователя'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Email подтвержден'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_type']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Profile(models.Model):
    """
    Профиль пользователя с дополнительной информацией
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Город'
    )
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return f"Профиль {self.user.username}"


class ExecutorProfile(models.Model):
    """
    Профиль исполнителя со специализацией и рейтингом
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='executor_profile',
        verbose_name='Исполнитель'
    )
    experience_years = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Опыт работы (лет)'
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость в час (руб.)'
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Средний рейтинг'
    )
    total_reviews = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Количество отзывов'
    )
    
    class Meta:
        verbose_name = 'Профиль исполнителя'
        verbose_name_plural = 'Профили исполнителей'
    
    def __str__(self):
        return f"Исполнитель {self.user.username}"
    
    def calculate_average_rating(self):
        """
        Пересчитывает средний рейтинг на основе отзывов
        """
        from reviews.models import Review
        reviews = Review.objects.filter(executor=self.user)
        if reviews.exists():
            total = sum(review.rating for review in reviews)
            self.average_rating = total / reviews.count()
            self.total_reviews = reviews.count()
            self.save()
        return self.average_rating
