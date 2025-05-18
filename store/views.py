from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def product_detail(request, id):
    return render(request, 'product.html', {'product_id': id})

def cart(request):
    return render(request, 'cart.html')