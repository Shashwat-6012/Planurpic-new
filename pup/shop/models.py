from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    cat_id = models.AutoField
    cat_name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.cat_name


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateTimeField()
    gender = models.CharField(
        max_length= 6,
        choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')],
        default='NONE'
    )
    user_address = models.CharField(max_length=500, default='NA')
    Phone_no = models.IntegerField(default='0')
    user_buyer = models.BooleanField(default = False)
    
    def __str__(self):
        return self.user.username

class BusinessUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Business_id = models.AutoField
    Business_contact = models.IntegerField()
    Business_email = models.CharField(max_length=50)
    Business_name = models.CharField(max_length=100)
    Business_address = models.TextField()
    Business_type = models.CharField(
        max_length= 11,
        choices=[('Trading', 'Trading'), ('Photography', 'Photography')],
        default='NONE'
    )

    def __str__(self):
        return self.user.username
    
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    product_category = models.ForeignKey(category, on_delete=models.CASCADE)
    product_subcategory = models.CharField(max_length=50, default= "")
    product_desc = models.CharField(max_length=500)
    product_price = models.FloatField(default=0)
    pub_date = models.DateField
    product_image = models.ImageField(upload_to = "shop/prod_images", default = "")
    product_seller = models.ForeignKey(BusinessUser, on_delete=models.CASCADE, default='00')

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['product_name']

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart_id = models.AutoField
    cart_items = models.TextField(default='NA')

    def __str__(self):
        return self.user.username + "'s Cart"

class Order(models.Model):
    order_id = models.IntegerField(primary_key='true')
    order_user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_items = models.TextField(default=" ")
    order_datetime = models.DateTimeField()
