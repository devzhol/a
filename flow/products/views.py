from django.shortcuts import render
from .models import Product


def home(request):
    products = Product.objects.all()

    return render(request, 'product.html', {
        'products': products
    })


def product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(request, 'product.html', {
        'product': product
    })