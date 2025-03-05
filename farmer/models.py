from django.db import models
from decimal import Decimal
# Create your models here.
class Farm_table(models.Model):
    nam=models.CharField(max_length=100)
    cnum=models.CharField(max_length=100)
    eml=models.CharField(max_length=100)
    password=models.CharField(max_length=100,default='website')
    anum=models.CharField(max_length=100)

       
    def __str__(self):
        return self.nam
class Prediction(models.Model):
    frmid=models.CharField(max_length=100)    
    prd=models.CharField(max_length=100)
    pic=models.FileField(upload_to="testimage")
    
    def __str__(self):
        return self.prd
class shop(models.Model):
    shname=models.CharField(max_length=100)   
    email=models.CharField(max_length=100)    
    passw=models.CharField(max_length=100)    
    location=models.CharField(max_length=100)    
    contact=models.CharField(max_length=100)  
    role=models.CharField(max_length=100,default='farmer')   
    def __str__(self):
        return self.shname
class Shopproduct(models.Model):
    pname=models.CharField(max_length=100)   
    cat=models.CharField(max_length=100)    
    brand=models.CharField(max_length=100)    
    price=models.CharField(max_length=100)    
    qty=models.CharField(max_length=100)
    image = models.ImageField(upload_to="products/")
    image2= models.ImageField(upload_to="products/")
    image3 = models.ImageField(upload_to="products/")
    image4 = models.ImageField(upload_to="products/")
    stock = models.PositiveIntegerField()
    description = models.TextField()
    shop = models.ForeignKey(shop, on_delete=models.CASCADE) 
    
    def __str__(self):
        return self.pname
    

# Farmer's Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    cat=models.CharField(max_length=100)
    qty=models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="frproducts/")
    image2= models.ImageField(upload_to="frproducts/")
    image3 = models.ImageField(upload_to="frproducts/")
    image4 = models.ImageField(upload_to="frproducts/")
    stock = models.PositiveIntegerField()
    farmer = models.ForeignKey(shop, on_delete=models.CASCADE)  # Farmer who added the product

    def __str__(self):
        return self.name

class NewCart(models.Model):
    user=models.ForeignKey(shop,on_delete=models.CASCADE)
    product=models.ForeignKey(Shopproduct,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def total_price(self):
        return( Decimal(self.product.price) * Decimal(self.quantity))
       
    
# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(shop, on_delete=models.CASCADE,related_name="cart_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="cart_product")
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        print(int(self.quantity) * 1234)
        return( Decimal(self.product.price) * Decimal(self.quantity))
class FarmerCart(models.Model):
    user = models.ForeignKey(shop, on_delete=models.CASCADE,related_name="cart_farmer")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="cart_farmer")
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        print(int(self.quantity) * 1234)
        return( Decimal(self.product.price) * Decimal(self.quantity))    

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]
    user = models.ForeignKey(shop, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(NewCart)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

# Delivery Model
class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    estimated_time = models.DateTimeField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Delivery for Order {self.order.id}"
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Card', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('NetBanking', 'Net Banking'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(shop, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"    