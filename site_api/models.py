from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя позиции')
    article = models.CharField(
        max_length=6,
        unique=True,
        validators=[RegexValidator(r'^\w{1,6}$', 'Article must be up to 6 alphanumeric characters.')],
        verbose_name='Артикул'
    )
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Цена')
    material = models.TextField(verbose_name='Материал')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='Категории')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Каталог'

    def __str__(self):
        return f"{self.name} ({self.article})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name='Фото')
    is_main = models.BooleanField(default=False, verbose_name='Основное фото?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Картинка товара'
        verbose_name_plural = 'Картинки товаров'
        constraints = [
            models.UniqueConstraint(
                fields=['product_id'],
                condition=models.Q(is_main=True),
                name='one_main_image_per_product'
            )
        ]

    def __str__(self):
        return f"Картинка для {self.product.name} ({'Основная' if self.is_main else 'Дополнительная'})"

class Look(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название образа')
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')
    products = models.ManyToManyField(Product, related_name='looks', verbose_name='Товары')
    categories = models.ManyToManyField(Category, related_name='looks', verbose_name='Категории')

    class Meta:
        db_table = 'looks'
        verbose_name = 'Образ'
        verbose_name_plural = 'Образы'

    def __str__(self):
        return self.name

class LookImage(models.Model):
    look = models.ForeignKey(Look, related_name='images', on_delete=models.CASCADE, verbose_name='Образ')
    image = models.ImageField(upload_to='look_images/', null=True, blank=True, verbose_name='Фото')
    is_main = models.BooleanField(default=False, verbose_name='Основное фото?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    class Meta:
        db_table = 'look_images'
        verbose_name = 'Картинка образа'
        verbose_name_plural = 'Картинки образов'
        constraints = [
            models.UniqueConstraint(
                fields=['look_id'],
                condition=models.Q(is_main=True),
                name='one_main_image_per_look'
            )
        ]

    def __str__(self):
        return f"Картинка для {self.look.name} ({'Основная' if self.is_main else 'Дополнительная'})"