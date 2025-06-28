from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from site_api.models import Product, ProductImage, Look, LookImage
from site_api.serializers import ProductSerializer, LookSerializer, LookImageSerializer

class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all().prefetch_related('images', 'categories')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductImageCreateView(APIView):
    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('is_main', False):
                product.images.filter(is_main=True).update(is_main=False)
            ProductImage.objects.create(product=product, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LookListCreateView(APIView):
    def get(self, request):
        looks = Look.objects.all().prefetch_related('images', 'products', 'categories')
        serializer = LookSerializer(looks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LookDetailView(APIView):
    def get(self, request, pk):
        try:
            look = Look.objects.get(pk=pk)
        except Look.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LookSerializer(look)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            look = Look.objects.get(pk=pk)
        except Look.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LookSerializer(look, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            look = Look.objects.get(pk=pk)
        except Look.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        look.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LookImageCreateView(APIView):
    def post(self, request, look_id):
        try:
            look = Look.objects.get(pk=look_id)
        except Look.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LookImageSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data.get('is_main', False):
                look.images.filter(is_main=True).update(is_main=False)
            LookImage.objects.create(look=look, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)