from django.contrib import admin

# Register your models here.
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.models import Group
from accounts.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
     list_display = ('id', 'email', 'account_id', 'postal_code', 'address', 'phone_number', 'created_at', 'updated_at')
     search_fields = ('email', 'account_id')
     list_filter = ('created_at', 'updated_at')

class UserAdmin(admin.ModelAdmin):
     list_display = ('id', 'email', 'account_id', 'postal_code', 'address', 'phone_number', 'created_at', 'updated_at')
     search_fields = ('email', 'account_id')
     list_filter = ('created_at', 'updated_at')

admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします

