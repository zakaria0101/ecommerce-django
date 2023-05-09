from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.models import User

from store.models import Cart, Order, OrderItem, Product,Profile


@login_required(login_url='login')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price += item.product.priceSell * item.product_qty

    userProfile = Profile.objects.filter(user=request.user).first()

    context = {'cartitems': cartitems, 'total_price': total_price,'userprofile':userProfile}
    return render(request, "store/checkout.html", context)


@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name :
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()
        
        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.country = request.POST.get('country')
            userprofile.city = request.POST.get('city')
            userprofile.zipcode = request.POST.get('zipcode')
            userprofile.save()


        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.country = request.POST.get('country')
        neworder.city = request.POST.get('city')
        neworder.zipcode = request.POST.get('zipcode')
        neworder.address = request.POST.get('address')

        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price += item.product.priceSell * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'no :' + str(random.randint(111111, 999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'no :' + str(random.randint(111111, 999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                Order=neworder,
                product=item.product,
                price=item.product.priceSell,
                quantity=item.product_qty
            )
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()
        Cart.objects.filter(user=request.user).delete()

        # return JsonResponse({'status': "Order Placed"})
    return redirect('/home')

