from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from store.models import Wishlist, Product


@login_required(login_url='login')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {'wishlist': wishlist}
    return render(request, "store/wishlist.html", context)


def addtowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            prod_check = Product.objects.get(id=prod_id)
            if(prod_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status': "Product Already in Wishlist"})
                else:
                    Wishlist.objects.create(
                        user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product Added to Wishlist successfully"})
            else:
                return JsonResponse({'status': "Product Not Found"})
        else:
            return JsonResponse({'status': "Login To Continue"})
    return redirect('/')


def deletewishlistitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                wishlistitem = Wishlist.objects.get(
                    product_id=prod_id, user=request.user)
                wishlistitem.delete()
                return JsonResponse({'status': "Product removed from your Wishlist"})
            else:
                return JsonResponse({'status': "Product Not found in Wishlist"})
        else:
            return JsonResponse({'status': "Login To Continue"})

    return redirect('/')
