from typing import Any
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import CategoryCreateForm, ReviewCreateForm, BrandCreateForm, MatchesWithCreateForm, ProductCreateForm, ProductUpdateForm, ReviewCreateForm
from .models import Category, Review, Brand, MatchesWith, Product

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
    
    
class ProductPage(ListView, CreateView):
    model = Product
    template_name = 'product_info.html'
    context_object_name = 'products'
    form_class = ReviewCreateForm
    
    def get_queryset(self):
        product_pk = self.kwargs['pk']
        product_info = Product.objects.filter(pk=product_pk)
        return product_info
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context