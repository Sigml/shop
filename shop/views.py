from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .forms import CategoryCreateForm, ReviewCreateForm, BrandCreateForm, MatchesWithCreateForm, ProductCreateForm, ProductUpdateForm
from .models import Category, Review, Brand, MatchesWith, Product

# Create your views here.
def main(request):
    return render(request, 'main.html')

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CategoryCreateView(AdminRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('category_create')


class CategoryListView(AdminRequiredMixin, ListView):
    model = Category
    template_name = 'all_category.html'
    context_object_name = 'object_list'


class CategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('category_all')


class BrandCreateView(AdminRequiredMixin, CreateView):
    model = Brand
    form_class = BrandCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('brand_create')


class BrandListView(AdminRequiredMixin, ListView):
    model = Brand
    template_name = 'all_brand.html'
    context_object_name = 'object_list'


class BrandDeleteView(AdminRequiredMixin, DeleteView):
    model = Brand
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('brand_all')


class MatchesWithCreateView(AdminRequiredMixin, CreateView):
    model = MatchesWith
    form_class = MatchesWithCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('matches_with_create')


class MatchesWithListView(AdminRequiredMixin, ListView):
    model = MatchesWith
    template_name = 'all_matches_with.html'
    context_object_name = 'object_list'


class MatchesWithDeleteView(AdminRequiredMixin, DeleteView):
    model = MatchesWith
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('matches_with_all')


class ProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'all_product.html'
    context_object_name = 'object_list'


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('product_create')


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('products_all')


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('products_all')