from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import CategoryCreateForm, ReviewCreateForm, BrandCreateForm, MatchesWithCreateForm, ProductCreateForm, ProductUpdateForm, ReviewCreateForm
from .models import Category, Review, Brand, MatchesWith, Product
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
    
    
    