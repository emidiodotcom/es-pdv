from django.contrib import admin

from .models import *


@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cashier', 'created_at', 'closed', 'total')
    list_filter = ('closed', 'created_at')
    search_fields = ('cashier__name',)
    inlines = [OrderProductInline, OrderPaymentInline]
