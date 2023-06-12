from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class item(models.Model):
    item_name = models.CharField(max_length=255)
    item_price = models.IntegerField(default=0)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name

class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True,editable=False)
    user_name=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    items=models.ForeignKey(item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    total_price=models.IntegerField(default=0)
    session_id = models.UUIDField(default=uuid.uuid4)
    


    def __str__(self):
        return str(self.cart_id)+" "+str(self.user_name)