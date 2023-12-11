
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

# Create your models here.


RATING= (
    (20, "★☆☆☆☆"),
    (40, "★★☆☆☆"),
    (60, "★★★☆☆"),
    (80, "★★★★☆"),
    (100, "★★★★★"),
)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345") #cid = category id
    title = models.CharField(max_length=100, default="Moveis") #titulo 
    image = models.ImageField(upload_to="category",default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="60" >' % (self.image.url) )
    
    def __str__(self):
        return self.title
    
    
class Product(models.Model):
     pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="prd", alphabet="abcdefgh12345") #pid = product id
     
     category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
     
     title = models.CharField(max_length=100, default="Cama") #titulo 
     image = models.ImageField(upload_to="product", default="product.jpg")
     description = models.TextField(null=True, blank=True, default="Produto")

     price = models.DecimalField(max_digits=999999, decimal_places=2,default="1.99")
     old_price = models.DecimalField(max_digits=999999, decimal_places=2,default="2.99")
     
     specifications = models.TextField(null=True, blank=True)
     stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
     

     status = models.BooleanField(default=True)
     in_stock = models.BooleanField(default=True)
     featured = models.BooleanField(default=False)

     sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
     
     class Meta:
        verbose_name_plural = "Products"
    
     def product_image(self):
            return mark_safe('<img src="%s" width="50" height="60" >' % (self.image.url) )
    
     def __str__(self):
        return self.title
     
     def get_percentage(self):
         new_price = 100 - (( self.price / self.old_price) * 100)
         return new_price
     
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images",default="product.jpg")
    product = models.ForeignKey(Product, related_name="p_images", on_delete= models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Product Images"

    
####################################### Cart order ########################################
####################################### Cart order ########################################
####################################### Cart order ########################################


class CartOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)   
    price = models.DecimalField(max_digits=999999, decimal_places=2,default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999, decimal_places=2,default="1.99")
    total = models.DecimalField(max_digits=999999, decimal_places=2,default="1.99")
    
    class Meta:
        verbose_name_plural = "Cart Order Items" 

    def oder_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="60" >' % (self.image) ) 
    
####################################### Wishlist & Reviews ########################################
####################################### Wishlist & Reviews ########################################
####################################### Wishlist & Reviews ########################################

    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"
    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"
    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    address = models.CharField(max_length=100, null= True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"    

