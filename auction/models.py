from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import time
import os
# Create your models here.


def product_imagepath(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_pics/user_<id>/<generated filename>
    parts = os.path.splitext(filename)
    ext = parts[1].lower() if len(parts) > 1 else ''
    return 'product_pics/user_{0}/{1}'.format(instance.user.id, f"{int(time.time())}{ext}")


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    description = models.CharField(max_length=200)
    image = models.ImageField(default='product_pics/default_product_pic.png', upload_to=product_imagepath)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.TextField(blank=True)  # use json.dumps to stringify the list of items

    def __str__(self):
        return str(self.user) + " Cart"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.TextField()  # use json.dumps to stringify the list of items
    total_amount = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.FloatField(validators=[MinValueValidator(0.0)])
    shipping_address = models.TextField()
    time_placed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s order at {self.time_placed}"


class Inventory(models.Model):
    item = models.OneToOneField(Product, on_delete=models.CASCADE)
    stock_count = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.item) + " Inventory"

    def in_stock(self):
        if self.stock_count <= 0:
            return False
        return True
