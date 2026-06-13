from django.contrib import admin
from .models import Game, Skin, Cart, CartItem, Order, OrderItem, Review


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'seller', 'price', 'rarity', 'condition', 'status', 'views', 'created_at', 'updated_at')
    list_filter = ('game', 'rarity', 'condition', 'status')
    search_fields = ('name', 'description', 'seller__username')
    readonly_fields = ('created_at', 'updated_at', 'views')
    list_editable = ('status', 'price')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Основна інформація', {
            'fields': ('game', 'seller', 'name', 'description', 'status')
        }),
        ('Характеристики', {
            'fields': ('rarity', 'condition', 'float_value')
        }),
        ('Ціна та медіа', {
            'fields': ('price', 'image', 'image_url')
        }),
        ('Статистика', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('buyer__username',)
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('skin', 'author', 'rating', 'created_at')
    list_filter = ('rating',)
    readonly_fields = ('created_at',)
