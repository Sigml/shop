from django.db import models
from users.models import CustomUser 

# Create your models here.
class Category(models.Model):
    name_category = models.CharField(max_length = 100)
    image_category = models.ImageField(upload_to='category_images/', null=True)


    def __str__(self):
        return self.name_category
    
    
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
    images = models.ImageField(upload_to='product_images/', default='default_image.jpg')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE)
    matches_with = models.ManyToManyField(MatchesWith)
    
        
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
    

class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    buy = models.BooleanField(default=False)
    
    
class DeliveryInfo(models.Model):
    SHIPPING_METHOD_CHOISES = [
        ('DHL', 'DHL'),
        ('Poczta polska', 'Poczta polska'),
        ('Fedex', 'Fedex'),
        ('Odbior w sklepie', 'Odbior w sklepie')
    ]
    
    METHOD_PAY_CHOICES = [
        ('przełew na konto', 'przełew na konto'),
        ('oplata za pobraniem', 'oplata za pobraniem'),
        ('BLIK', 'BLIK'),
        ('gotówka', 'gotówka')
    ]
    
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    shipping_method = models.CharField(max_length=255, choices=SHIPPING_METHOD_CHOISES)
    method_pay = models.CharField(max_length=50, choices=METHOD_PAY_CHOICES)
    is_delivered = models.BooleanField(default=False)
    
    def addres(self):
        if self.apartment_number is not None:
            return f'Województwo: {self.state}, kod pocztowy: {self.zip_code}, miasto: {self.city}, numer domu: {self.house_number}, numer mieszkania: {self.apartment_number}'
        else:
            return f'Województwo: {self.state}, kod pocztowy: {self.zip_code}, miasto: {self.city}, numer domu: {self.house_number}'
