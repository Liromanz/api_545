from rest_framework import serializers
from site_api.models import Product, ProductImage, Category, Look, LookImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'article', 'price', 'material', 'created_at', 'images', 'categories']

    def validate_images(self, value):
        main_images = [img for img in value if img.get('is_main', False)]
        if len(main_images) != 1:
            raise serializers.ValidationError("Exactly one image must be marked as main.")
        if not value:
            raise serializers.ValidationError("At least one image is required.")
        return value

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        categories_data = validated_data.pop('categories', [])
        product = Product.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        product.categories.set(categories_data)
        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        categories_data = validated_data.pop('categories', None)
        instance.name = validated_data.get('name', instance.name)
        instance.article = validated_data.get('article', instance.article)
        instance.price = validated_data.get('price', instance.price)
        instance.material = validated_data.get('material', instance.material)
        instance.save()

        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)
        if categories_data is not None:
            instance.categories.set(categories_data)
        return instance

class LookImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = LookImage
        fields = ['id', 'image', 'is_main', 'created_at']

class LookSerializer(serializers.ModelSerializer):
    images = LookImageSerializer(many=True)
    products = ProductSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Look
        fields = ['id', 'name', 'price', 'created_at', 'images', 'products', 'categories']

    def validate_images(self, value):
        main_images = [img for img in value if img.get('is_main', False)]
        if len(main_images) != 1:
            raise serializers.ValidationError("Exactly one image must be marked as main.")
        if not value:
            raise serializers.ValidationError("At least one image is required.")
        return value

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        products_data = validated_data.pop('products', [])
        categories_data = validated_data.pop('categories', [])
        look = Look.objects.create(**validated_data)
        for image_data in images_data:
            LookImage.objects.create(look=look, **image_data)
        look.products.set(products_data)
        look.categories.set(categories_data)
        return look

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        products_data = validated_data.pop('products', None)
        categories_data = validated_data.pop('categories', None)
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        if images_data:
            instance.images.all().delete()
            for image_data in images_data:
                LookImage.objects.create(look=instance, **image_data)
        if products_data is not None:
            instance.products.set(products_data)
        if categories_data is not None:
            instance.categories.set(categories_data)
        return instance