from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from order.models import Transaction,Order
from django.views.generic import FormView,ListView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout,update_session_auth_hash
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from order.models import CartItem
# from django.views.generic.edit import UpdateView
# Create your views here.
class UserRegistrationView(FormView):
    template_name='account/user_register.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('account')

    def form_valid(self,form):
        # print(form.cleaned_data)
        user=form.save()
        login(self.request,user)
        # print(user)
        messages.success(self.request,'You Have Registered Successfully')
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name="account/user_login.html"

    def form_valid(self,form):
        messages.success(self.request,'You Have Logged In Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')



@login_required
def user_update_view(request):
    user_form = UserUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    orders = Order.objects.filter(user=request.user).order_by('-placed_on')
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-timestamp')
    cart_items = None
    total_price=0
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)-sum(item.product.discount_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            messages.success(request, 'You Have Successfully Updated Your Account and Password!')
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, request.user)
            return redirect('account')
        elif user_form.is_valid():
            messages.success(request, 'You Have Successfully Updated Your Account!')
            user_form.save()
            return redirect('account')
        elif password_form.is_valid():
            messages.success(request, 'You Have Successfully Updated Your Password!')
            password_form.save()
            update_session_auth_hash(request, request.user)
            return redirect('account')

    return render(request, 'account/user_account.html', {
        'form': user_form,
        'password_form': password_form,
        'orders': orders,
        'transactions': transactions,
        'cart_items': cart_items,
        'total_price': total_price,
    })