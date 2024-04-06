"""Doctype"""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from product.models import Product, Category

from .forms import SignupForm

def get_products(category_slug=None, query=None):
    """
    Get products based on category slug and/or query.

    Args:
        category_slug (str, optional): The slug of the category to filter products.
        query (str, optional): The query string to filter products by name or description.

    Returns:
        QuerySet: A queryset containing products that match the given criteria.
    """
    # pylint: disable=no-member
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return products
    


def frontpage(request):
    """
    Render the front page with a list of latest products.
    """
    # pylint: disable=no-member
    products = Product.objects.all()[:15]
    return render(request, 'core/frontpage.html', {'products': products})

def signup(request):
    """
    Handle user sign-up process.

    This function processes the sign-up form submitted by the user.
    If the request method is POST, it attempts to validate the form data.
    If the form is valid, it creates a new user account and logs in the user.
    If the request method is GET, it renders the sign-up form for the user.

    Returns:
        HttpResponse: The HTTP response object rendering the sign-up form.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})


@login_required

def myaccount(request):
    """
    Render the user's account page.

    This function renders the user's account page, showing their profile information,
    orders, or any other relevant details.

    Returns:
        HttpResponse: The HTTP response object rendering the user's account page.
    """
    return render(request, 'core/myaccount.html')

@login_required
def edit_myaccount(request):

    """
    Handle editing user account information.

    This function allows a logged-in user to edit their account information.
    If the request method is POST, the user's information is updated with the form data.
    If the request method is GET, the edit profile form is rendered.

    Returns:
        HttpResponse: The HTTP response object rendering the edit profile form or redirecting
        to the user's account page after successful update.
    """
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('myaccount')
    return render(request, 'core/edit_myaccount.html')


def shop(request):
    """
    Render the shop page with product listings.

    This function renders the shop page, displaying product listings based on
    the selected category and search query.

    Returns:
        HttpResponse: The HTTP response object rendering the shop page.
    """
    # pylint: disable=no-member
    categories = Category.objects.all()
    active_category = request.GET.get('category', '')
    query = request.GET.get('query', '')

    products = get_products(category_slug=active_category, query=query)

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category,
        'query': query
    }

    return render(request, 'core/shop.html', context)

def about(request):
    """
    Render the about page.

    This function renders the about page, providing information about the website,
    company, or any other relevant details.

    Returns:
        HttpResponse: The HTTP response object rendering the about page.
    """
    return render(request, 'core/about.html')
