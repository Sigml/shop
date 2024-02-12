from django.db.models.query import QuerySet
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import (CategoryCreateForm, ReviewCreateForm, BrandCreateForm, MatchesWithCreateForm, ProductCreateForm, ProductUpdateForm, ReviewCreateForm,
                AddToCartForm, DeliveryInfoForm)
from .models import Category, Review, Brand, MatchesWith, Product, OrderItem, DeliveryInfo
from users.models import CustomUser
# Create your views here.

class CategoryMainListView(ListView):
    model = Category
    template_name = 'main.html'
    context_object_name = 'all_category'
    

def main(request):
    category_list_view = CategoryMainListView.as_view()
    return category_list_view(request)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CategoryAdminCreateView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('category_create')
    
    
class CategoryAdminUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('category_all')


class CategoryAdminListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = 'all_category.html'
    context_object_name = 'object_list'


class CategoryAdminDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('category_all')


class BrandAdminCreateView(AdminRequiredMixin, CreateView):
    model = Brand
    form_class = BrandCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('brand_create')


class BrandAdminListView(AdminRequiredMixin, ListView):
    model = Brand
    template_name = 'all_brand.html'
    context_object_name = 'object_list'


class BrandAdminDeleteView(AdminRequiredMixin, DeleteView):
    model = Brand
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('brand_all')


class MatchesWithAdminCreateView(AdminRequiredMixin, CreateView):
    model = MatchesWith
    form_class = MatchesWithCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('matches_with_create')


class MatchesWithAdminListView(AdminRequiredMixin, ListView):
    model = MatchesWith
    template_name = 'all_matches_with.html'
    context_object_name = 'object_list'


class MatchesWithAdminDeleteView(AdminRequiredMixin, DeleteView):
    model = MatchesWith
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('matches_with_all')


class ProductAdminListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'all_product.html'
    context_object_name = 'object_list'


class ProductAdminCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('product_create')


class ProductAdminUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('products_all')


class ProductAdminDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('products_all')
    
    
class ProductInCategoryListView(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        category_name = self.kwargs['category']
        category_products = Product.objects.filter(category__name_category=category_name)

        sorted_products = sorted(category_products, key=lambda x: not x.is_featured)
        
        return sorted_products

   
class ProductPageListView(ListView):
    model = Product
    template_name = 'product_info.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_name = self.kwargs['category']
        product_pk = self.kwargs['pk']
        product_info = Product.objects.filter(category__name_category=category_name, pk=product_pk)
        return product_info


class ProductPageReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'form.html'
    form_class = ReviewCreateForm

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_info', kwargs={'category': self.kwargs.get('category'), 'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_page_review'] = self
        return context


class AddToCartViev(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        form = AddToCartForm()
        context = {
            'form':form,
            'product':product
        }
        return render(request, 'add_to_cart.html', context)
    
    def post(self, request,pk, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product = Product.objects.get(pk=pk)
            price = product.price
            OrderItem.objects.create(user=request.user, product=product, quantity=quantity, price=price)
            return redirect('cart')
    
    
    
class ShoppingCartView(LoginRequiredMixin, View):
    template_name = 'cart.html'
    
    def get(self, request, *args, **kwargs):
        cart_items = OrderItem.objects.filter(user=request.user, buy=False)
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.quantity * item.product.price for item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_quantity':total_quantity,
            'total_price':total_price,
        }

        return render(request, self.template_name, context)
    
    
    
class DeleteShoppingCartDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('cart')
    
    
class DeliveryInfoCreateView(LoginRequiredMixin, CreateView):
    model = DeliveryInfo
    form_class = DeliveryInfoForm
    template_name = 'delivery_info.html'
    success_url = reverse_lazy('delivery_succes')
    
    def form_valid(self, form):
        form.instance.order_item = get_object_or_404(OrderItem, pk=self.kwargs['order_item_id'])
        return super().form_valid(form)


class DeliverySuccesSendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = OrderItem.objects.filter(user=request.user, buy=False)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        delivery_info = DeliveryInfo.objects.filter(order_item=cart_items.first()).latest('id')

        
        subject = 'Potwierdzenie zamówienia'
        message = f'Dziękujemy za złożenie zamówienia.\n\n'
        message += f'Twoje zamówienie:\n'
        for item in cart_items:
            message += f'- {item.product.name} (ilość: {item.quantity})\n'
        message += f'Koszt zamówienia: {total_price}\n\n'
        message += f'Dane odbiorcy:\n'
        message += f'Imię i nazwisko: {delivery_info.recipient_name}\n'
        message += f'Adres dostawy: {delivery_info.addres()}'
    
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = [request.user.email]
        
        send_mail(subject, message, sender_email, recipient_email, fail_silently=False)  
        
        for item in cart_items:
            product = item.product
            if item.quantity > product.stock_quantity:
                return HttpResponse('Zamówiono więcej produktu niż jest dostępne w magazynie.')
            product.stock_quantity -= item.quantity
            product.save()
            
            
        for item in cart_items:
            item.buy = True
            item.save()
            
        return redirect('main')    
