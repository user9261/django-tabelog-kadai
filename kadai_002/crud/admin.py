from django.contrib import admin
from .models import Restaurant,Category,Subscription,Review,Favorite
from django.utils.safestring import mark_safe

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business_hours', 'start_time', 'end_time', 'zip_code', 'address', 'phone_number', 'price_range', 'category', 'image')
    search_fields = ('name',)
    list_filter = ('category',)
     
    def image(self, obj):
        return mark_safe('<img src="{}" style="width:100px height:auto;">'.format(obj.img.url))
   
 
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('name',)

class SubscriptionAdmin(admin.ModelAdmin):
     list_display = ('id', 'stripe_subscription_id', 'stripe_customer_id',)
     search_fields = ('stripe_subscription_id',)

class ReviewAdmin(admin.ModelAdmin):
     list_display = ('id', 'restaurant', 'content',)
     search_fields = ('restaurant',)    

class FavoriteAdmin(admin.ModelAdmin):
     list_display = ('id', 'restaurant',)
     search_fields = ('restaurant',)    


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Favorite, FavoriteAdmin)

