"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from users.views import (RegisterView, LoginView, LogoutView, EmailVerifyView, ResetPasswordView, ResetPasswordV2View, UserInfoView,
                        UserProfileUpdateView )
from shop.views import (main, CategoryAdminCreateView, CategoryAdminListView, CategoryAdminDeleteView, BrandAdminListView, BrandAdminCreateView, BrandAdminDeleteView, 
                        MatchesWithAdminListView, MatchesWithAdminCreateView, MatchesWithAdminDeleteView, ProductAdminListView, ProductAdminCreateView, 
                        ProductAdminDeleteView, ProductAdminUpdateView, ProductInCategoryListView, CategoryAdminUpdateView, ProductPageListView, 
                        ProductPageReviewCreateView, AddToCartViev, ShoppingCartView
                        )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('add_to_cart/<int:pk>/', AddToCartViev.as_view(), name='add_to_cart'),
    path('cart/', ShoppingCartView.as_view(), name='cart'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    path('confirm_email/', TemplateView.as_view(template_name='confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerifyView.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='invalid_verify.html'), name='invalid_verify'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password/<uidb64>/<token>/', ResetPasswordV2View.as_view(), name='reset_password'),
    path('user/info/', UserInfoView.as_view(), name='user_info'),
    path('user/update/', UserProfileUpdateView.as_view(), name='user_update'),
    path('category_create/', CategoryAdminCreateView.as_view(), name='category_create'),
    path('category_all/', CategoryAdminListView.as_view(), name='category_all'),
    path('category_update/<int:pk>', CategoryAdminUpdateView.as_view(), name= 'category_update'),
    path('category_delete/<int:pk>/', CategoryAdminDeleteView.as_view(), name='category_delete'),
    path('brand_all/', BrandAdminListView.as_view(), name='brand_all'),
    path('brand_create/', BrandAdminCreateView.as_view(), name='brand_create'),
    path('brand_delete/<int:pk>/', BrandAdminDeleteView.as_view(), name='brand_delete'),
    path('matches_with_all/', MatchesWithAdminListView.as_view(), name='matches_with_all'),
    path('matches_with_create/', MatchesWithAdminCreateView.as_view(), name='matches_with_create'),
    path('matches_with_delete/<int:pk>/', MatchesWithAdminDeleteView.as_view(), name='matches_with_delete'),
    path('products_all/', ProductAdminListView.as_view(), name='products_all'),
    path('product_create/', ProductAdminCreateView.as_view(), name='product_create'),
    path('product_delete/<int:pk>/', ProductAdminDeleteView.as_view(), name='product_delete'),
    path('product/update/<int:pk>/', ProductAdminUpdateView.as_view(), name='product_update'),
    path('<category>/', ProductInCategoryListView.as_view(), name='products'),
    path('<category>/<int:pk>/', ProductPageListView.as_view(), name='product_info'),
    path('<category>/<pk>/review/', ProductPageReviewCreateView.as_view(), name='product_review'),


]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)