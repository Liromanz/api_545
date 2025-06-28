from django.contrib import admin
from django import forms
from django.forms import FileInput
from django.utils.html import format_html
from django.db import models
from site_api.models import Product, ProductImage, Category, Look, LookImage


class NonClearableFileInput(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = {**self.attrs, **(attrs or {})}
        return super().render(name, value, attrs, renderer)


class MultiFileInput(FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = {**self.attrs, **(attrs or {}), 'multiple': True}
        return super().render(name, value, attrs, renderer)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ['image_preview', 'image', 'is_main']
    readonly_fields = ['image_preview']
    formfield_overrides = {
        models.ImageField: {'widget': NonClearableFileInput},
    }

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Превью'


class LookImageInline(admin.TabularInline):
    model = LookImage
    extra = 0
    fields = ['image_preview', 'image', 'is_main']
    readonly_fields = ['image_preview']
    formfield_overrides = {
        models.ImageField: {'widget': NonClearableFileInput},
    }

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'


class ProductAdminForm(forms.ModelForm):
    main_image = forms.ImageField(label="Основное фото", required=False)
    additional_images = forms.FileField(
        label="Дополнительные фото",
        widget=MultiFileInput(),
        required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'article', 'price', 'material', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        main_image = cleaned_data.get('main_image')
        if not self.instance.pk and not main_image:
            raise forms.ValidationError("Основное фото обязательно при создании товара.")
        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        product.save()

        # Сохранение основного фото
        if self.cleaned_data.get('main_image'):
            ProductImage.objects.filter(product=product, is_main=True).delete()
            ProductImage.objects.create(
                product=product,
                image=self.cleaned_data['main_image'],
                is_main=True
            )

        # Сохранение дополнительных фото
        if self.files.getlist('additional_images'):
            for image in self.files.getlist('additional_images'):
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_main=False
                )

        if commit:
            self.save_m2m()

        return product

class LookAdminForm(forms.ModelForm):
    main_image = forms.ImageField(label="Основное фото", required=False)
    additional_images = forms.FileField(
        label="Дополнительные фото",
        widget=MultiFileInput(),
        required=False
    )

    class Meta:
        model = Look
        fields = ['name', 'price', 'products', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        main_image = cleaned_data.get('main_image')
        if not self.instance.pk and not main_image:
            raise forms.ValidationError("Основное фото обязательно при создании образа.")
        return cleaned_data

    def save(self, commit=True):
        look = super().save(commit=False)
        look.save()

        # Сохранение основного фото
        if self.cleaned_data.get('main_image'):
            LookImage.objects.filter(look=look, is_main=True).delete()
            LookImage.objects.create(
                look=look,
                image=self.cleaned_data['main_image'],
                is_main=True
            )

        # Сохранение дополнительных фото
        if self.files.getlist('additional_images'):
            for image in self.files.getlist('additional_images'):
                LookImage.objects.create(
                    look=look,
                    image=image,
                    is_main=False
                )

        if commit:
            self.save_m2m()  # Сохраняем продукты и категории

        return look


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['main_image_preview', 'article', 'name', 'price', 'material']
    list_display_links = ['main_image_preview', 'article', 'name']
    list_filter = ['categories']
    search_fields = ['name', 'article', 'categories__name']
    filter_horizontal = ['categories']
    inlines = [ProductImageInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images', 'categories')

    def main_image_preview(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            return format_html('<img src="{}" width="50" height="50" />', main_image.image.url)
        return "No main image"
    main_image_preview.short_description = 'Основное фото'

    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Количество фото'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__name', 'product__article']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Превью'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


@admin.register(Look)
class LookAdmin(admin.ModelAdmin):
    form = LookAdminForm
    list_display = ['main_image_preview', 'name', 'price']
    list_display_links = ['main_image_preview', 'name']
    list_filter = ['created_at', 'categories']
    search_fields = ['name', 'categories__name', 'products__name', 'products__article']
    filter_horizontal = ['products', 'categories']
    inlines = [LookImageInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images', 'products', 'categories')

    def main_image_preview(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            return format_html('<img src="{}" width="50" height="50" />', main_image.image.url)
        return "Нет изображения"
    main_image_preview.short_description = 'Основное фото'


@admin.register(LookImage)
class LookImageAdmin(admin.ModelAdmin):
    list_display = ['look', 'image_preview', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['look__name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'