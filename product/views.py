"""Doctype"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError

from .models import Product

def product(request, slug):
    """
    Display details of a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the product to be displayed.

    Returns:
        HttpResponse: The HTTP response object rendering the product details page.
    """
    try:
        product = get_object_or_404(Product, slug=slug) # pylint: disable=W0621
        return render(request, 'product/product.html', {'product': product})
    except Product.MultipleObjectsReturned: # pylint: disable=E1101
        return HttpResponseServerError("Product doesn't exist")
