from django.urls import path
from site_api.views import ProductListCreateView, ProductDetailView, ProductImageCreateView, LookListCreateView, LookDetailView, LookImageCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/images/', ProductImageCreateView.as_view(), name='product-image-create'),
    path('looks/', LookListCreateView.as_view(), name='look-list-create'),
    path('looks/<int:pk>/', LookDetailView.as_view(), name='look-detail'),
    path('looks/<int:look_id>/images/', LookImageCreateView.as_view(), name='look-image-create'),
] 