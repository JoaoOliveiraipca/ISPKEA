from django.contrib import admin
from core.models import Product, Category, CartOrderItems, CartOrder, Wishlist,ProductImages, Address, ProductReview

# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'product_image', 'category', 'price', 'featured', "in_stock"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class CartOderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date']

class CartOderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty','price','total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product' ,'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(CartOrder,CartOderAdmin)
admin.site.register(CartOrderItems,CartOderItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Address,AddressAdmin)
        