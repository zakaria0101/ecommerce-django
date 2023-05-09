from django.urls import path
from . import views
from store.controller import authview, cart, wishlist, checkout

urlpatterns = [
    path('home', views.home, name="home"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:slug>', views.collectionsview, name="collectionsview"),
    path('collections/<str:cat_slug>/<str:prod_slug>',
         views.productview, name="productview"),

    path('product-list',views.prodlist),
    
    path("searchproduct", views.searchproduct, name="searchproduct"), #name tag of the input


    path('register/', authview.register, name="register"),
    path('login/', authview.loginpage, name="login"),
    path('logout/', authview.logoutpage, name="logout"),

    path('add-to-cart', cart.addtocart, name="addtocart"),
    path('cart', cart.viewcart, name="cart"),
    path('update-cart', cart.updateCart, name='updateCart'),
    path('delete-cart-item', cart.deletecartproduct, name='deletecartproduct'),

    path('wishlist', wishlist.index, name='wishlist'),
    path('add-to-wishlist', wishlist.addtowishlist, name='addtowishlist'),
    path('delete-wishlist-item',wishlist.deletewishlistitem, name='deletewishlistitem'),

    path('checkout', checkout.index, name="checkout"),
    path('place-order', checkout.placeorder, name="placeorder"),
]
