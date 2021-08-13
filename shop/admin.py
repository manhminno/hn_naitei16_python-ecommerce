from django.contrib import admin
from .models import CustomUser, Category, Product, Image, Size, ProductSize, Order, Item, Sale, SaleProduct, Comment

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'create_at', 'update_at', 'is_active')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent')
    

class ImageInline(admin.TabularInline):
    model = Image
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description', 'activate')
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('url', 'product')
    

admin.site.register(Size)
    

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'amount')
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'status', 'create_at', 'approve_at')
    

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'size', 'amount', 'price')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('value', 'type', 'description')


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'content', 'replyComment', 'create_at', 'update_at')
