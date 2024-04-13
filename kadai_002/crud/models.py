from django.db import models
from django.urls import reverse
 
class Category(models.Model):
     name = models.CharField(max_length=200)
 
     def __str__(self):
         return self.name

class Restaurant(models.Model):
     name = models.CharField(max_length=200)
     business_hours = models.CharField(max_length=200)
     zip_code = models.CharField(max_length=200)
     address = models.CharField(max_length=200,default='愛知県')
     phone_number = models.CharField(max_length=200)
     min_price = models.PositiveIntegerField(default=0)
     max_price = models.PositiveIntegerField(default=0)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     img = models.ImageField(blank=True, default='noImage.png')

     def __str__(self):
        return self.name
    
     # 新規作成・編集完了時のリダイレクト先
     def get_absolute_url(self):
        return reverse('list')