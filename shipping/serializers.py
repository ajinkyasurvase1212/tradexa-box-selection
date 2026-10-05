from rest_framework import serializers

from .models import Product, Order, OrderItem


class OrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Product does not exist."
            )

        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "items"]
        read_only_fields = ["id", "created_at"]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one product is required."
            )

        return value

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create()

        for item_data in items_data:
            product = Product.objects.get(
                id=item_data["product_id"]
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data["quantity"],
            )

        return order