from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, ExecutorProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Админ-панель для пользователей
    """
    list_display = ('username', 'email', 'user_type', 'is_verified', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('user_type', 'is_verified')}),
    )
    
    actions = ['block_users', 'unblock_users']
    
    def block_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'Заблокировано пользователей: {queryset.count()}')
    block_users.short_description = 'Заблокировать выбранных пользователей'
    
    def unblock_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'Разблокировано пользователей: {queryset.count()}')
    unblock_users.short_description = 'Разблокировать выбранных пользователей'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель для профилей
    """
    list_display = ('user', 'phone', 'city')
    search_fields = ('user__username', 'phone', 'city')
    list_filter = ('city',)


@admin.register(ExecutorProfile)
class ExecutorProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель для профилей исполнителей
    """
    list_display = ('user', 'experience_years', 'hourly_rate', 'average_rating', 'total_reviews')
    search_fields = ('user__username',)
    list_filter = ('experience_years',)
    readonly_fields = ('average_rating', 'total_reviews')
