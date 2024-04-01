from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect

from product.models import Product, Category

from .forms import SignupForm

def get_products(category_slug=None, query=None):
    products = Product.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return products


def frontpage(request):
    
    products = Product.objects.all()[:15]
    return render(request, 'core/frontpage.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            return redirect('/')
    else:
        form = SignupForm()
    
    return render(request, 'core/signup.html', {'form': form})
    
def login_old(request):
    return render(request, 'core/login.html')
    
def shop(request):
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