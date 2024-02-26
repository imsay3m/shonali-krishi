from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from order.models import Transaction
from django.views.generic import FormView,ListView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout,update_session_auth_hash
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
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

class UserUpdateView(LoginRequiredMixin,View):
    template_name = 'account/user_account.html'

    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': user_form,'password_form':password_form})

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            messages.success(self.request,'You Have Successfully Updated Your Account and Password!')
            user_form.save()
            password_form.save()
            return redirect('account')
        elif user_form.is_valid():
            messages.success(self.request,'You Have Successfully Updated Your Account!')
            user_form.save()
            return redirect('account')
        elif password_form.is_valid():
            messages.success(self.request,'You Have Successfully Updated Your Password!')
            password_form.save()
            return redirect('account')
        return redirect('account')



#-----------------------------------------------------------------------------------

""" class UserUpdateView(UpdateView):
    template_name = 'account/user_account.html'
    model=UserAccount
    form_class=UserUpdateForm
    pk_url_kwarg='id'


    def get_success_url(self):
        messages.success(self.request, "profile update successfully")
        return reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': user_form}) """
    
#-----------------------------------------------------------------------------------

""" def form_valid(self,form):
        user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        
        messages.success(self.request,'You Have Successfully Updated Your Account!')
        user_form.save()
        return redirect('account')
        # return redirect('account')  """
#-----------------------------------------------------------------------------------
"""     def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            messages.success(self.request,'You Have Successfully Updated Your Account!')
            user_form.save()
            return redirect('account')
        return redirect('account')  """


#-----------------------------------------------------------------------------------

""" def change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(
                    request, pass_form.user
                )  # pass will get updated
                messages.success(request, "Password Changed Successfully")
                return redirect("profile")
        else:
            pass_form = PasswordChangeForm(user=request.user)
        return render(request, "account/account.html", {"password_form": password_form})
    else:
        messages.warning(request, "Please Log In to Your Account")
        return redirect("login") """

#-----------------------------------------------------------------------------------

class PaymentReportView(ListView, LoginRequiredMixin):
    template_name = 'account/user_account.html'
    model = Transaction
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        ).order_by('-timestamp')
        return queryset