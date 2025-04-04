import uuid
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from .forms import ProductForm  # Не забудьте создать файл forms.py с ProductForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'store/manage_users.html', {'users': users})


@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    return render(request, 'store/admin_panel.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def product_create(request):
    # Только для пользователей с правами staff
    if not request.user.is_staff:
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form})

def product_edit(request, id):
    # Только для пользователей с правами staff
    if not request.user.is_staff:
        return redirect('product_list')
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form})

def add_to_cart(request, product_id):
    """Добавление товара в корзину (данные хранятся в сессии)."""
    cart = request.session.get('cart', {})
    # Увеличиваем количество товара, если он уже есть в корзине
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def cart_view(request):
    """Отображение корзины."""
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_sum = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        total_price = product.price * quantity
        total_sum += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price,
        })
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_sum': total_sum,
    })

def checkout(request):
    """Оформление покупки: для каждого товара создается заказ с общим номером, корзина очищается."""
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    # Генерируем общий номер заказа для всех товаров в одной покупке
    order_number = str(uuid.uuid4())[:8]
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            order_number=order_number
        )
    # Очищаем корзину после оформления заказа
    request.session['cart'] = {}
    return redirect('profile')
def delete_product(request, product_id):
    if not request.user.is_staff:
        return redirect('product_list')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'store/manage_users.html', {'users': users})
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)  # Только админы могут управлять пользователями
def manage_users(request):
    users = User.objects.all()
    return render(request, 'store/manage_users.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)  
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        return redirect('manage_users')  # Запрещаем удаление суперпользователей
    user.delete()
    return redirect('manage_users')
