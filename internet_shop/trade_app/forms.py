from django import forms
from django.utils.translation import ugettext_lazy

from trade_app.models import Product, Comment, Specification


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'logo', 'description', 'min_price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
        }
        labels = {
            'min_price': ugettext_lazy('Price from'),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
        }


class SpecificationForm(forms.ModelForm):

    class Meta:
        model = Specification
        fields = '__all__'
