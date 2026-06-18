from django.contrib import admin
from .models import *

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

# Inline for Rent Images
class RentImageInline(admin.TabularInline):
    model = RentImage
    extra = 1  # Number of empty forms to display

class RentAdmin(admin.ModelAdmin):
    inlines = [RentImageInline]

# Register models
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)  # Product should be registered with the inline
admin.site.register(Wishlist)
admin.site.register(Rent, RentAdmin)  # Rent should be registered with the inline
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(CarContact)
admin.site.register(CarSubmission)

# Note: You can remove the registration for ProductImage if you only want it to be accessible through ProductAdmin.
# admin.site.register(ProductImage)  # Remove this line if you don't want separate registration
