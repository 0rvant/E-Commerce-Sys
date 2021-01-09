from django.contrib import admin
from .models import *

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'rate', 'status', 'create_at']
    list_filter = ['status']
    readonly_fields = ['subject', 'comment', 'rate', 'user', 'product','ip']

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(WishList)
admin.site.register(WishListItem)
admin.site.register(ShippingAddress)
admin.site.register(Review, ReviewAdmin)