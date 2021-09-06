from django.test import TestCase, Client
from django.urls import reverse
from shop.models import CustomUser, Image, Item, Order, Product,Category, ProductSize, Size, Comment, Sale, SaleProduct
from ..utils.constant import LENGTH_PAGE, STATUS_ORDER, FILTER, SALE

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        test_user1 = CustomUser.objects.create_user(email= 'test1@gmail.com', username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = CustomUser.objects.create_user(email= 'test2@gmail.com', username='testuser2', password='2HJ1vRV0Z&3iD')
        category = Category.objects.create(name="Category test 1", description="Description for category test 1")
        product = Product.objects.create(name= "Product test 1", category= category, price= 500000.0, description= 'Product for category test 1')
        image1 = Image.objects.create(url = "jum5_1.jpg", product = product)
        image2 = Image.objects.create(url = "jum5_2.jpg", product = product)
        image3 = Image.objects.create(url = "jum5_3.jpg", product = product)
        image4 = Image.objects.create(url = "jum5_4.jpg", product = product)
        image5 = Image.objects.create(url = "jum5_5.jpg", product = product)
        obj = Order.objects.create(user = test_user1, status = STATUS_ORDER['not_paid'])
        obj2 = Order.objects.create(user = test_user1, status = STATUS_ORDER['waitting'])
        size = Size.objects.create(description='XL')
        item = Item.objects.create(order = obj, product = product, size = size)
        item2 = Item.objects.create(order = obj2, product = product, size = size)
        self.order = obj2
        self.product = product
        test_user1.save()
        test_user2.save()


    def test_product_list_GET(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_list.html')

    def test_product_detail_GET(self):
        response = self.client.get(reverse('shop:product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('shop:add_to_cart', kwargs={'pk': self.product.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_add_to_cart(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:add_to_cart', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)
        
    def test_remove_cart(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:remove_cart', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)
        
    def test_update_cart(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:update_cart', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)
        
    def test_payment(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:payment'))
        self.assertEqual(response.status_code, 302)
    
    def test_cancel_order(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:cancel_order',kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)
    
    def test_add_to_wishlist(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:user_wishlist', kwargs={'id': self.product.pk}))
        self.assertEqual(response.status_code, 302)
    
    def test_remove_from_wishlist(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('shop:remove_to_wishlist', kwargs={'id': self.product.pk}))
        self.assertEqual(response.status_code, 302)
