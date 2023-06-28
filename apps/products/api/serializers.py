from rest_framework import serializers

from apps.products.models import Category, Product, Promotion


class CategorySerializer(serializers.ModelSerializer):
    # publicId = serializers.CharField(source="public_id", read_only=True)

    class Meta:
        model = Category
        fields = ["name", "slug"]
        read_only_fields = ["name", "slug"]


class PromotionSerializer(serializers.ModelSerializer):
    # publicId = serializers.CharField(source="public_id", read_only=True)
    # discountedPrice = serializers.FloatField(source="discounted_price", read_only=True)
    isExpiredDiscount = serializers.SerializerMethodField(read_only=True)
    startDate = serializers.DateTimeField(source="start_date", read_only=True)
    endDate = serializers.DateTimeField(source="end_date", read_only=True)

    def get_isExpiredDiscount(self, obj: Promotion) -> bool:
        return obj.is_expired_discount()

    class Meta:
        model = Promotion
        fields = [
            # "publicId",
            "title",
            "discount",
            # "discountedPrice",
            "isExpiredDiscount",
            "startDate",
            "endDate",
        ]
        read_only_fields = ["title", "discount"]


class ProductSerializer(serializers.ModelSerializer):
    publicId = serializers.CharField(source="public_id", read_only=True)
    price = serializers.FloatField(read_only=True)
    category = CategorySerializer(read_only=True)
    promotion = PromotionSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Product
        fields = [
            "publicId",
            "name",
            "slug",
            "stock",
            "price",
            "promotion",
            "category",
            "description",
            "thumbnail",
            "createdAt",
            "updatedAt",
        ]
        read_only_fields = ["name", "slug", "stock", "description", "thumbnail"]
