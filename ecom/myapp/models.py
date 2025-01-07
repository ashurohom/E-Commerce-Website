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