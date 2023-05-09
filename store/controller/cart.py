from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store.models import Product, Cart


def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            prod_check = Product.objects.get(id=prod_id)
            if(prod_check):
                if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status': "Product Already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if prod_check.InStock >= prod_qty:
                        Cart.objects.create(
                            user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product Added successfully"})
                    else:
                        return JsonResponse({'status': "Only" + str(prod_check.InStock) + ""})
            else:
                return JsonResponse({'status': "Product Not Found"})
        else:
            return JsonResponse({'status': "Login To Do this Action"})
    return redirect('/')


@login_required(login_url='login')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {'cart': cart}
    return render(request, "store/cart.html", context)


def updateCart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status': 'Quantity Updated'})
    return redirect('/')


def deletecartproduct(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            cartitem = Cart.objects.get(product_id=prod_id, user=request.user)

            cartitem.delete()
        return JsonResponse({'status': "Product deleted from your cart"})
    return redirect('/')
