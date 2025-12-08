from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'executor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer__username', 'executor__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['hide_reviews']
    
    def hide_reviews(self, request, queryset):
        # Можно добавить поле is_hidden в модель
        self.message_user(request, f'Скрыто отзывов: {queryset.count()}')
    hide_reviews.short_description = 'Скрыть выбранные отзывы'
