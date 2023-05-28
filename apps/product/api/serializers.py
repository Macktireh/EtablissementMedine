from rest_framework import serializers

from apps.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)

    class Meta:
        model = Category
        fields = ["publicId", "name", "slug"]
        read_only_fields = ["name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    price = serializers.FloatField(read_only=True)
    priceDiscount = serializers.FloatField(source="price_discount", read_only=True)
    expiryDiscount = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    category = CategorySerializer(read_only=True)

    def get_expiryDiscount(self, obj: Product) -> str:
        return obj.is_expired_discount()

    class Meta:
        model = Product
        fields = [
            "publicId",
            "name",
            "slug",
            "stock",
            "price",
            "discount",
            "priceDiscount",
            "expiryDiscount",
            "description",
            "thumbnail",
            "category",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = ["name", "slug", "stock", "price", "discount", "description", "thumbnail"]
