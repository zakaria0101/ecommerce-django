from django.shortcuts import render,redirect
from django.contrib import messages
from  .models import *
from django.http import JsonResponse
 
# Create your views here.

def home(request):
    return render(request, "store/index.html")

def collections(request):
    category = Category.objects.filter()
    context = {'category':category}
    return render(request, "store/collections.html",context)


def collectionsview(request,slug):
    if(Category.objects.filter(slug=slug)):
        prod = Product.objects.filter(subcategory__slug=slug)
        cname = Category.objects.filter(slug=slug).first()
        context = {'prod' : prod,'cname':cname}
        return render(request, "store/products/index.html",context)
    else:
        messages.warning(request, "category not found ")
        return redirect('collections')
    
def productview(request,cat_slug,prod_slug ):
    if(Category.objects.filter(slug=cat_slug)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            prod = Product.objects.filter(slug=prod_slug,status=0).first
            context = {'prod':prod}
        else:
            messages.error(request,"Product not found")
            return redirect('collections')
    else:
        messages.error(request,"Category not found")
        return redirect('collections')
    return render(request, "store/products/info.html", context)

def prodlist(request):
    products = Product.objects.filter(status=0).values_list('name', flat=True)
    prodlist = list(products)

    return JsonResponse(prodlist, safe=False)

def searchproduct(req):
    if req.method == 'POST':
        q = req.POST.get('productsearch')
        product = Product.objects.filter(name__contains=q).first()
        if product:
            return redirect('collections/'+product.subcategory.slug+'/'+product.slug)
        else:
            messages.info(req, "No product found with that name")
            return redirect(req.META.get('HTTP_REFERER'))
    return redirect(req.META.get('HTTP_REFERER'))
