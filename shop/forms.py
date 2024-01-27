from .models import Category, Review, Brand, MatchesWith, Product
from django import forms
from django.forms import CharField, TextInput, ChoiceField, Select, ClearableFileInput, CheckboxInput, SelectMultiple



class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name_category', 'image_category')
        widgets = {
            'name_category': TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Nazwa Kategorii'
            }),
            'image_category':ClearableFileInput(attrs={
                'class':'form-control',
            }),
        }


class ReviewCreateForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    class Meta:
        model = Review
        fields = ('user', 'text', 'rating')
        widgets = {
            'text': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'opinia'
            }),
            'rating': Select(attrs={
                'class': 'form-control'
            },choices='RATING_CHOICES')
        }


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name_brand', 'image_brand')
        widgets = {
            'name_brand': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa brendu'
            }),
            'image_brand': ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }

    def clean_image_brand(self):
        image_brand = self.cleaned_data.get('image_brand', False)
        if not image_brand:
            raise forms.ValidationError("To pole jest wymagane.")
        return image_brand


class MatchesWithCreateForm(forms.ModelForm):
    class Meta:
        model=MatchesWith
        fields = ('name_product',)
        widgets = {
            'name_product': TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Pasuje do produktu o nazwie'
            })
        }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'description', 'category', 'images', 'stock_quantity', 'brand', 'matches_with', 'is_featured')
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa produktu'
            }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cena'
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opis produktu'
            }),
            'category': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoria'
            }),
            'images': ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'stock_quantity': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ilość na stanie'
            }),
            'brand': Select (attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa brendu'
            }),
            'matches_with': SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Pasuje do...'
            }),
            'is_featured': CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price','discount_price', 'description', 'category', 'images', 'stock_quantity', 'brand', 'matches_with', 'is_featured')
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa produktu'
            }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cena'
            }),
            'discount_price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Promocijna cena'
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opis produktu'
            }),
            'category': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoria'
            }),
            'images': ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'stock_quantity': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ilość na stanie'
            }),
            'brand': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa brendu'
            }),
            'matches_with': SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Pasuje do...'
            }),
            'is_featured': CheckboxInput(attrs={
                'class': 'form-check-input',
            })

        }
        

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'rating')
        widgets = {
            'text': TextInput(attrs={
                'class':'form-control',
                'placeholder': 'Komentarz'
            }),
            'rating': Select(attrs={
                'class':'form-control'
            })
        }
    