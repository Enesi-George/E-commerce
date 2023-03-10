from django.shortcuts import render
from django.http import JsonResponse
import json 
from .models import *


# Create your views here.

def index(request):
    return render(request, "main/home.html")

def welcome(request):
    return render(request, "main/dashboard.html")

def store(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items #to show numbers of item ordered behind the cart basket
	else:
		items = []
		order = {'get_cart_items': 0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']

	products = Product.objects.all() 
	context = {'products': products, 'cartItems': cartItems}
	return render(request, "main/store.html", context)

def cart(request): 
	if request.user.is_authenticated: #i.e if the user is logged in
		customer = request.user.customer # we get the user from the one2one relationship we created, save it as customer
		order, created = Order.objects.get_or_create(customer = customer, complete=False) # querying the customers Order from Model
		items = order.orderitem_set.all() #from the model, getting the child due one to many relatn btw order(as the parent) and OrderItem (child)
		cartItems = order.get_cart_items #to show numbers of item ordered behind the cart basket

	else:	#if user is non_authenticated
		items =[]
		order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']


	context = {"items":items, 'order':order, 'cartItems':cartItems}
	return render(request, "main/cart.html", context)

def checkout(request):
	if request.user.is_authenticated: #i.e if the user is logged in
		customer = request.user.customer # we get the user from the one2one relationship we created, save it as customer
		order, created = Order.objects.get_or_create(customer = customer, complete=False) # querying the Order from Model
		items = order.orderitem_set.all() #from the model, getting the child due one to many relatn btw order(as the parent) and OrderItem (child)
		cartItems = order.get_cart_items #to show numbers of item ordered behind the cart basket

	else:	#if user is non_authenticated
		items =[]
		order = {'get_cart_total':0, 'get_cart_items': 0, 'shipping': False}
		cartItems = order['get_cart_items']
	context = {"items":items, 'order':order, 'cartItems':cartItems}
	return render(request, "main/checkout.html", context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('productId:', productId)
 
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer = customer, complete=False)
	
	orderItem, created = OrderItem.objects.get_or_create(order= order, product = product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('item was added', safe = False)

