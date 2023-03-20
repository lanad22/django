from django.shortcuts import render
from django.http import JsonResponse
import json

from .models import * 
from .forms import CommentForm

def mystore(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items


	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'mystore/mystore.html', context)

def cart(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	cartItems = order.get_cart_items
	
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'mystore/cart.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def product_detail(request, id):
    customer = request.user.customer
    product = Product.objects.get(id=id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                product=product
            )
            comment.save()

    comments = Comment.objects.filter(product=product)
    context = {
        'product': product,
        'cartItems':cartItems,
        "comments": comments,
        'form': form
    }
    return render(request, 'mystore/detail.html', context)