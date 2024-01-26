from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import CategoryCreateForm, ReviewCreateForm, BrandCreateForm, MatchesWithCreateForm, ProductCreateForm, ProductUpdateForm
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
        return Product.objects.filter(category__name_category=category_name)