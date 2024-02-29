from django.db import transaction,IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from .models import CartItem,Order,Transaction
from product.models import Product
from django.contrib import messages

# Create your views here.

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)-sum(item.product.discount_price * item.quantity for item in cart_items)
    return render(request, 'order/cart.html', {'cart_items': cart_items, 'total_price': total_price})
@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity += quantity
    cart_item.save()
    return redirect('view_cart')
@login_required
def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('view_cart')
@login_required
def item_increment(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
@login_required
def item_decrement(request, id):
    cart_item = get_object_or_404(CartItem, id=id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')
@login_required
def cart_clear(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)-sum(item.product.discount_price * item.quantity for item in cart_items)
    return render(request, 'order/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
@transaction.atomic
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items) - sum(item.product.discount_price * item.quantity for item in cart_items)

    user_account = request.user.account
    if user_account.balance < total_price:
        messages.error(request, "Insufficient balance in your account.")
        return redirect('account')
    try:
        with transaction.atomic():
            # Deduct the total amount from the user's account balance
            user_account.balance -= total_price
            user_account.save()

            # Create a transaction record for the payment
            transaction_record = Transaction.objects.create(
                account=user_account,
                transaction_type='PAY',
                amount=total_price,
                balance_after_transaction=user_account.balance
            )

            # Generate payment_id based on the primary key
            payment_id = 100000 + transaction_record.pk
            transaction_record.payment_id = payment_id
            transaction_record.save()

            # Create an order with the purchased items
            order = Order.objects.create(
                user=request.user,
                total=total_price,
                status='New Orders',
            )

            # Generate order_no based on the primary key
            order_no = 100000 + order.pk
            order.order_no = order_no
            order.save()

            for cart_item in cart_items:
                product = cart_item.product
                product.buyer.add(request.user)
                order.products.add(cart_item.product)

            # Clear the user's cart
            cart_items.delete()

    except IntegrityError:
        messages.error(request, "An error occurred while processing your order. Please try again later.")
        return redirect('view_cart')


    messages.success(request, "Order placed successfully!")
    return redirect('account')  # Redirect to account


