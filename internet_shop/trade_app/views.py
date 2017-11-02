from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views import generic
from django.urls import reverse_lazy

from trade_app.models import Product, Comment, Specification
from trade_app.forms import ProductForm, CommentForm, SpecificationForm, ProductSearchForm


# All about Products ----------------------------
class ProductsListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'

    def get_queryset(self):
        attrs = self.request.GET
        if attrs.get('car_name'):
            queryset = Product.objects.filter(name__icontains=attrs.get('car_name'))
        elif len(attrs) > 1:
            # to group data by using distinct .order_by('product_id').distinct('product_id')
            specs = Specification.objects.filter(
                name__icontains=attrs.get('name'),
                mark__icontains=attrs.get('mark'),
                model__icontains=attrs.get('model'),
                engine_type__icontains=attrs.get('engine_type'),
                transmission__icontains=attrs.get('transmission')
            )
            if attrs.get('gearbox'):
                specs = specs.filter(
                    specifications__gearbox=int(attrs.get('gearbox'))
                )
            queryset = Product.objects.filter(pk__in=specs.values('product_id'))
        else:
            queryset = super(ProductsListView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['search_form'] = ProductSearchForm()
        return context


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
    model = Specification
    form_class = SpecificationForm
    template_name = 'specification_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class SpecificationsDeleteView(generic.DeleteView):
    model = Specification
    success_url = reverse_lazy('cars:products_list')
