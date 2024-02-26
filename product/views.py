from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from .models import Product,Category
from django.views.generic  import DetailView
from django.core.paginator import Paginator
from .form import ReviewForm
# Create your views here.
def product(request,category_slug=None):
    data=Product.objects.all()
    paginator=Paginator(data,9)
    page_number=request.GET.get('page')
    final_data=paginator.get_page(page_number)
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        data = Product.objects.filter(categories=category)
        paginator=Paginator(data,9)
        page_number=request.GET.get('page')
        final_data=paginator.get_page(page_number)
    category=Category.objects.all()
    return render(request,'product/products.html',{'products':final_data,'categories':category})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_details.html'
    pk_url_kwarg = 'id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        reviews = product.reviews.all()
        review_form=ReviewForm()
        context["form"] = review_form
        context["reviews"] = reviews
        return context

    def post(self, request,*args, **kwargs):
        product = self.get_object()
        form = ReviewForm(self.request.POST)

        if form.is_valid():
            user = self.request.user
            if user in product.buyer.all():
                form.instance.user = user
                form.instance.product = product
                form.save()
                messages.success(self.request,"You have successfully submitted the review")
                return HttpResponseRedirect(reverse('product_details', kwargs={'id': product.pk}))
        messages.error(request,"In order to review, you have to buy first")
        return HttpResponseRedirect(reverse('product_details', kwargs={'id': product.pk}))