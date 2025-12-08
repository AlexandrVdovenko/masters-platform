from django.contrib import admin
from .models import PortfolioItem, PortfolioImage


class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'executor', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'executor__username')
    inlines = [PortfolioImageInline]


@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ('portfolio_item', 'caption')
    search_fields = ('portfolio_item__title', 'caption')
