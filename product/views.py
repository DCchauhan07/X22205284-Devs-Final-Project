from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError

from .models import Product

def product(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'product/product.html', {'product': product})
    except Product.MultipleObjectsReturned:
        return HttpResponseServerError("Product doesn't exist")
