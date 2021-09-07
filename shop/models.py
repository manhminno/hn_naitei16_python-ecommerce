from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.urls import reverse
import datetime

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=254)
    address = models.CharField(max_length=254,null=True)
    create_at = models.DateField(null=True, blank=True, default=datetime.date.today)
    update_at = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()


class Category(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, null=True)
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:category', args=[str(self.id)]) 


class Product(models.Model):
    name = models.CharField(max_length=254)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0)
    activate = models.BooleanField(default=True)
    description = models.CharField(max_length=254, null=True)
    users_wishlist = models.ManyToManyField('CustomUser', related_name="user_wishlist", blank=True)

    def __str__(self):
        return self.name     
    
    def get_absolute_url(self):
        return reverse('shop:product-detail', args=[str(self.id)]) 
    
    def get_add_to_cart_url(self):
        return reverse('shop:add_to_cart', args=[str(self.id)])


class Image(models.Model):
    url = models.CharField(max_length=254)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)


class Size(models.Model):
    description = models.CharField(max_length=254)

    def __str__(self):
        return self.description 


class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey('Size', on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=0)


class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    create_at = models.DateField(null=True, blank=True, default=datetime.date.today)
    approve_at = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    
    LOAN_STATUS = (
        ('p', 'Paid'),
        ('n', 'Not paid'),
        ('w', 'waitting'),
        ('c','Cancel'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='n',
    )

    def get_cancel_order_url(self):
        return reverse('shop:cancel_order', args=[str(self.id)])
    
    def get_finish_order_url(self):
        return reverse('shop:finish_order', args=[str(self.id)])


class Item(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey('Size', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True)
    price = models.FloatField(null=True)
    amount = models.IntegerField(default=0)

    def get_remove_cart_url(self):
        return reverse('shop:remove_cart', args=[str(self.id)])
    
    def get_update_cart_url(self):
        return reverse('shop:update_cart', args=[str(self.id)])


class Sale(models.Model):
    value = models.FloatField()
    description = models.CharField(max_length=254, null=True)
    url = models.CharField(max_length=254,null=True,blank=True)
    LOAN_TYPE = (
        ('p', 'Percent'),
        ('d', 'Direct'),
    )

    type = models.CharField(
        max_length=1,
        choices=LOAN_TYPE,
        blank=True,
        default='p',
    )


class SaleProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    sale = models.ForeignKey('Sale', on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=254)
    replyComment = models.ForeignKey('Comment', on_delete=models.SET_NULL, null=True, blank=True)
    create_at = models.DateField(null=True, blank=True, default=datetime.date.today)
    update_at = models.DateField(null=True, blank=True)
    rate = models.IntegerField(default=1)
