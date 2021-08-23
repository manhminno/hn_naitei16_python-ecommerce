from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='product_list'),
    path('category/<int:pk>/', views.ShopView.as_view(), name='category'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('search', views.product_search, name='product_search'),
    path('cart_detail', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:pk>', views.remove_cart, name='remove_cart'),
    path('update_cart/<int:pk>', views.update_cart, name='update_cart'),
    path('payment', views.add_payment, name='payment'),
    path('payment_detail', views.payment_detail, name='payment_detail'),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel_order'),
    path('cancel_order_detail', views.cancel_order_detail, name='cancel_order_detail'),
    path('history_order', views.history_order, name='history_order'),
    path('detail-profile', views.detail_profile, name='detail-profile'),
    path('logout', views.user_logout, name='logout'),
    url('signup', views.signup, name='signup'),
    path('change-password', views.change_password, name='change-password'),
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
    path("wishlist/remove_to_wishlist/<int:id>", views.remove_from_wishlist, name="remove_to_wishlist"),
]
