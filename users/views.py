# from django.contrib.auth.backends import UserModel
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator as token_generator, default_token_generator
from django.utils.http import urlsafe_base64_decode
from .utils import send_email_verify, send_email_reset_password
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.edit import FormView
from .forms import UserCreationForm, LoginForm, SeachUserForm, ResetPasswordForm, UserProfileUpdateForm
from .models import CustomUser
from django.urls import reverse_lazy

import logging

logger = logging.getLogger(__name__)


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                password = data.pop('password_confirmation')

                user = CustomUser.objects.create_user(**data)
                user.set_password(password)
                send_email_verify(request, user)
                user.save()
                return redirect('confirm_email')
            return render(request, 'registration.html', {'form':form})
        except IntegrityError as e:
                return HttpResponseServerError('Użytkownik już istnieje')
        except Exception as e:
                logger.error(f"Error during user registration: {e}")
                message = "Coś poszło nie tak, spróbuj ponownie później"
                return render(request, 'registration.html', {'message': message})


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        print(f"UIDB64: {uidb64}, Token: {token}")

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            login(request, user)
            return redirect('main')
        
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
    

class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = CustomUser.objects.authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect(self.success_url)
            else:
                form.add_error(None, 'Nieprawidłowy email lub hasło')
                messages.error(request, 'Nieprawidłowy email lub hasło')


        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('main')


class ResetPasswordView(View):
    def get(self, request):
        form = SeachUserForm()
        return render(request, 'seach_user.html', {'form': form})
    
    def post(self, request):
        form = SeachUserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_exists = CustomUser.objects.filter(email=cleaned_data['email']).first()
            if user_exists:
                send_email_reset_password(request, user_exists)
                return render(request, 'confirm_email.html')
            else:
                form.add_error(None, 'Nieprawidłowy email')
                messages.error(request, 'Nieprawidłowy email')

                return render(request, 'seach_user.html', {'form': form})
            
            
class ResetPasswordV2View(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        form = ResetPasswordForm()

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            return render(request, 'reset_password.html', {'form':form})
        
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            CustomUser.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user
    
    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        form = ResetPasswordForm(request.POST)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user.set_password(cleaned_data['password'])
                user.save()
                login(request, user)

                return redirect ('main')
            
            else:
                return render(request, 'reset_password.html', {'form':form})
            
        else:
            return redirect ('invalid_verify')
            

class UserInfoView(View):
    def get (self, request):
        if request.user.is_authenticated:
            user_info = {
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'date_of_birth': request.user.date_of_birth,
                'number_phone': request.user.number_phone,
                'profile_picture': request.user.profile_picture,
                'description': request.user.description,
            }

            return render(request, 'user_info.html', {'form': user_info})

        else:
            return redirect('login')
        
# class UserProfileUpdateView(View):
#     def get (self, request):
#         form = UserProfileUpdateForm()
#         return render (request, 'user_update.html', {'form':form})
    
#     def post (self, request):
#         model = CustomUser
#         form = UserProfileUpdateForm(request.POST)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             user = request.user

#             user.username = cleaned_data['username']
#             user.email = cleaned_data['email']
#             user.first_name = cleaned_data['first_name']
#             user.last_name = cleaned_data['last_name']
#             user.number_phone = cleaned_data['number_phone']
#             user.date_of_birth = cleaned_data['date_of_birth']
#             user.description = cleaned_data['description']

#             user.save()

#             return redirect('user_info')
#         else:
#             messages.error(request, 'Formularz jest nieprawidłowy. Sprawdź wprowadzone dane.')
        
#         return render(request, 'user_update.html', {'form':form})
            
class UserProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('user_info')
    
    def get_object(self, queryset=None):
        return self.request.user