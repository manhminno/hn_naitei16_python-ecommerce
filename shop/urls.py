from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='product_list'),
    path('category/<int:pk>/', views.ShopView.as_view(), name='category'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('detail-profile', views.detail_profile, name='detail-profile'),
    path('logout', views.user_logout, name='logout'),
    url('signup', views.signup, name='signup'),
]
