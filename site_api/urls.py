from django.urls import path
from site_api.views import ProductListCreateView, ProductDetailView, ProductImageCreateView

app_name = 'site_api'

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/images/', ProductImageCreateView.as_view(), name='product-image-create'),
]