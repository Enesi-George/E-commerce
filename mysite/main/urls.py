from django.urls import path
from . import views


urlpatterns =[
path("home/", views.index, name="index"),
path("dashboard/", views.welcome, name="dashboard"),
path("store/", views.store, name="store"),
path("cart/", views.cart, name="cart"),
path("checkout/", views.checkout, name="checkout"),
path("update_item/", views.updateItem, name="updateItem"), 

]