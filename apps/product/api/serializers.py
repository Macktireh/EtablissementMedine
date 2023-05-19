from rest_framework import serializers

from apps.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ["publicId", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2, min_value=0.00)
    stock = serializers.IntegerField(read_only=True)
    description = serializers.CharField(read_only=True)
    thumbnail = serializers.CharField(read_only=True)
    categoryId = serializers.CharField(source="category.public_id", read_only=True)

    class Meta:
        model = Product
        exclude = ["id", "public_id", "category"]
