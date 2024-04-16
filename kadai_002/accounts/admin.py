from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Restaurant, RestaurantAdmin)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします

