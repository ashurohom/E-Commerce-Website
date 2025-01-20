from django.db import models

# Create your models here.
class Product(models.Model):
    CAT=((1,"shoes"),(2,"mobile"),(3,"cloths"),(4,"watch"))
    pname = models.CharField(max_length=50)
    price = models.FloatField()
    category = models.IntegerField(choices=CAT, verbose_name="Product Name")
    description = models.CharField(max_length=300, verbose_name="Details")
    is_active = models.BooleanField(default=True, verbose_name="Is_Available")
    image = models.ImageField(upload_to='image')
    offer_price = models.IntegerField(default=0)

    def __str__(self):
        return self.pname

class Card(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid') #direct access table not a cloumn
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid') 
    qty=models.IntegerField(default=1)   


class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
    p_id=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()

    def __str__(self):
        return self.order_id # it return the only char value to the admin interface and user inetrface
    
    
class Address(models.Model):
    userid = models.ForeignKey("auth.User",on_delete=models.CASCADE, db_column="userid")
    address = models.CharField(max_length=100)    
    fullname = models.CharField(max_length=50)    
    city = models.CharField(max_length=30)    
    pincode = models.CharField(max_length=10)    
    state = models.CharField(max_length=30)    
    mobile = models.CharField(max_length=10)    

class History(models.Model):
    order_id = models.ForeignKey('Order',on_delete=models.CASCADE, db_column="order_id")
    userid = models.ForeignKey("auth.User",on_delete=models.CASCADE, db_column="userid")
    amount=models.FloatField()
    address = models.CharField(max_length=300)
    status = models.CharField(max_length=30)
    

    

