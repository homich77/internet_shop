from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views import generic
from django.urls import reverse_lazy

from trade_app.models import Product, Comment, Specification
from trade_app.forms import ProductForm, CommentForm, SpecificationForm


# All about Products ----------------------------
class ProductsListView(generic.ListView):
    model = Product


class ProductsDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductsDetailView, self).get_context_data(**kwargs)
        product = get_object_or_404(
            Product.objects.prefetch_related('specifications', 'comments'),
            id=self.kwargs.get('pk')
        )
        context['product'] = product
        context['comment_form'] = CommentForm()
        return context


class ProductsCreateView(generic.CreateView):
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProductsUpdateView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProductsDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy('cars:products_list')


@require_http_methods(['POST'])
def product_add_comment_view(request, pk):
    product = Product.objects.get(id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.product = product
        instance.save()
    return redirect(product)


# All about Specifications ----------------------
class SpecificationsCreateView(generic.CreateView):
    form_class = SpecificationForm
    template_name = 'specification_form.html'
    success_url = reverse_lazy('cars:products_list')


class SpecificationsDetailView(generic.DetailView):
    model = Specification


class SpecificationsUpdateView(generic.UpdateView):
    form_class = SpecificationForm
    template_name = 'specification_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class SpecificationsDeleteView(generic.DeleteView):
    model = Specification

    # def get_success_url(self):
    #     return reverse_lazy(
    #         'cars:product_details',
    #         kwargs={'pk': self.kwargs.get('id')}
    #     )
