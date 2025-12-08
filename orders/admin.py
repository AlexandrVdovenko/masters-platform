from django.contrib import admin
from .models import Category, Order, Response


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-панель для категорий
    """
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ-панель для заказов
    """
    list_display = ('title', 'customer', 'category', 'status', 'budget_min', 'budget_max', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'customer__username')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    actions = ['mark_as_deleted']
    
    def mark_as_deleted(self, request, queryset):
        queryset.update(status='deleted')
        self.message_user(request, f'Удалено заказов: {queryset.count()}')
    mark_as_deleted.short_description = 'Пометить как удаленные'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """
    Админ-панель для откликов
    """
    list_display = ('order', 'executor', 'proposed_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__title', 'executor__username', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
