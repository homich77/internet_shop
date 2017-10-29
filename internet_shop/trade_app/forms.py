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


class ProductSearchForm(forms.Form):
    GEARBOX = (
        ('', 'all'),
        (4, 'four-speed'),
        (5, 'five-speed'),
        (6, 'six-speed'),
    )
    TYPE_OF_TRANSMISSION = (
        ('', 'all'),
        ('MT', 'manual transmission'),
        ('AT', 'automatic transmission')
    )
    name = forms.CharField(max_length=64, required=False)
    mark = forms.CharField(max_length=32, required=False)
    model = forms.CharField(max_length=32, required=False)
    engine_type = forms.CharField(max_length=64, required=False)
    gearbox = forms.ChoiceField(choices=GEARBOX, required=False)
    transmission = forms.ChoiceField(choices=TYPE_OF_TRANSMISSION, required=False)
