from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings  # 追加

 
class Category(models.Model):
     name = models.CharField(max_length=200)
 
     def __str__(self):
         return self.name
     
class Restaurant(models.Model):
     name = models.CharField(max_length=200)
     business_hours = models.CharField(default=None, max_length=200)
     start_time = models.CharField(default=None, max_length=200)
     end_time = models.CharField(default=None, max_length=200)
     zip_code = models.CharField(max_length=200)
     address = models.CharField(max_length=200,default='愛知県')
     phone_number = models.CharField(max_length=200)
     price_range = models.CharField(max_length=200)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     img = models.ImageField(blank=True, default='noImage.png')

     def __str__(self):
        return self.name
    
     # 新規作成・編集完了時のリダイレクト先
     def get_absolute_url(self):
        return reverse('top')
     
# crud/models.py

class Subscription(models.Model):
      user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
      stripe_subscription_id = models.CharField(max_length=255, blank=True)
      stripe_customer_id = models.CharField(max_length=255, blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def __str__(self):
         return f"{self.user.username}'s Subscription"
      
class Favorite(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
      restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')

      def __str__(self):
         return f"{self.user.username}'s Favorite"
      
class Reservation(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
      restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reserved_by')
      reservation_date = models.DateField(null=True)
      reservation_time = models.TimeField(null=True)
      number_of_people = models.IntegerField(default=None)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)

      def __str__(self):
         return f"{self.user.username}'s Reservation at {self.restaurant.name}"
      
class Review(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
      restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviewed_by')
      content = models.CharField(max_length=255, blank=True)

      def __str__(self):
         return f"{self.user.username}'s Review"




