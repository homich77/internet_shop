from django.conf.urls import url

from trade_app.views import *

urlpatterns = [
    url(r'^$', ProductsListView.as_view(), name='products_list'),
    url(r'^create/$', ProductsCreateView.as_view(), name='products_create'),
    url(r'^(?P<pk>[0-9]+)/$', ProductsDetailView.as_view(), name='product_details'),
    url(r'^(?P<pk>[0-9]+)/update/$', ProductsUpdateView.as_view(), name='products_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', ProductsDeleteView.as_view(), name='product_delete'),
    url(r'^(?P<pk>[0-9]+)/add_comment/$', product_add_comment_view, name='products_add_comment'),
    url(r'^spec/create/$', SpecificationsCreateView.as_view(), name='spec_create'),
    url(r'^spec/(?P<pk>[0-9]+)/$', SpecificationsDetailView.as_view(), name='spec_details'),
    url(r'^spec/(?P<pk>[0-9]+)/update/$', SpecificationsUpdateView.as_view(), name='spec_update'),
    url(r'^spec/(?P<pk>[0-9]+)/delete/$', SpecificationsDeleteView.as_view(), name='spec_delete'),
]
