from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, CartItem
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    cart_count = CartItem.objects.filter(session_id=request.session.session_key).count()
    return render(request, 'index.html', {'products': products, 'cart_count': cart_count})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_count = CartItem.objects.filter(session_id=request.session.session_key).count()
    return render(request, 'product.html', {'product': product, 'cart_count': cart_count})

def cart(request):
    if not request.session.session_key:
        request.session.create()
    cart_items = CartItem.objects.filter(session_id=request.session.session_key)
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    cart_count = cart_items.count()
    # Add item_total to each cart item
    for item in cart_items:
        item.item_total = item.product.price * item.quantity
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count
    })

def add_to_cart(request, product_id):
    if not request.session.session_key:
        request.session.create()
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        session_id=request.session.session_key,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Added to cart!')
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, session_id=request.session.session_key)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')

from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings

def send_email_view(request):
    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            subject='Message from Your Site',
            message=message,
            from_email=settings.EMAIL_HOST_USER,  # Replace with your email
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        return render(request, 'send_email.html', {'success': True})
    
    return render(request, 'send_email.html')
