from django.db import models
from users.models import CustomUser 

# Create your models here.
class Category(models.Model):
    name_category = models.CharField(max_length = 100)


    def __str__(self):
        return self.name_category
    
    
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.rating}"
    
    
class Brand(models.Model):
    name_brand = models.CharField(max_length=50)
    image_brand = models.ImageField(upload_to='brand_images/')
    

    def __str__(self):
        return self.name_brand
    
    
    def image_url(self):
        return self.image_brand.url


class MatchesWith(models.Model):
    name_product = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name_product


class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.FloatField(max_length = 10)
    discount_price = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length = 500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    stock_quantity = models.PositiveIntegerField(default=0)
    reviews = models.ManyToManyField(Review)
    is_featured = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    matches_with = models.ManyToManyField(MatchesWith)
