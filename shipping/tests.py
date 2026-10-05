from django.test import TestCase
from rest_framework.test import APIClient

from .models import Product, Box
from .services import dimensions_fit, find_suitable_box


class BoxSelectionTests(TestCase):

    def setUp(self):
        self.small_box = Box.objects.create(
            name="Small Box",
            internal_length=20,
            internal_width=20,
            internal_height=20,
            max_weight=5,
            cost=50,
        )

        self.medium_box = Box.objects.create(
            name="Medium Box",
            internal_length=30,
            internal_width=30,
            internal_height=30,
            max_weight=10,
            cost=80,
        )

        self.large_box = Box.objects.create(
            name="Large Box",
            internal_length=50,
            internal_width=50,
            internal_height=50,
            max_weight=25,
            cost=120,
        )

    def test_product_fits_in_box(self):
        result = dimensions_fit(
            (10, 10, 10),
            (20, 20, 20)
        )

        self.assertTrue(result)

    def test_product_does_not_fit_in_box(self):
        result = dimensions_fit(
            (30, 30, 30),
            (20, 20, 20)
        )

        self.assertFalse(result)

    def test_product_can_fit_after_rotation(self):
        result = dimensions_fit(
            (25, 10, 10),
            (10, 25, 10)
        )

        self.assertTrue(result)

    def test_cheapest_suitable_box_is_selected(self):
        product = Product.objects.create(
            name="Laptop",
            length=15,
            width=10,
            height=5,
            weight=2,
        )

        from .models import Order, OrderItem

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        selected_box = find_suitable_box(order)

        self.assertEqual(
            selected_box.name,
            "Small Box"
        )

    def test_heavy_product_selects_larger_box(self):
        product = Product.objects.create(
            name="Heavy Product",
            length=10,
            width=10,
            height=10,
            weight=7,
        )

        from .models import Order, OrderItem

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        selected_box = find_suitable_box(order)

        self.assertEqual(
            selected_box.name,
            "Medium Box"
        )

    def test_no_box_when_product_is_too_large(self):
        product = Product.objects.create(
            name="Large Product",
            length=100,
            width=100,
            height=100,
            weight=5,
        )

        from .models import Order, OrderItem

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
        )

        selected_box = find_suitable_box(order)

        self.assertIsNone(selected_box)

    def test_multiple_products_can_fit_in_box(self):
        laptop = Product.objects.create(
            name="Laptop",
            length=15,
            width=10,
            height=5,
            weight=2,
        )

        mouse = Product.objects.create(
            name="Mouse",
            length=10,
            width=8,
            height=5,
            weight=0.5,
        )

        from .models import Order, OrderItem

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=laptop,
            quantity=1,
        )

        OrderItem.objects.create(
            order=order,
            product=mouse,
            quantity=2,
        )

        selected_box = find_suitable_box(order)

        self.assertIsNotNone(selected_box)
        self.assertEqual(
            selected_box.name,
            "Small Box"
        )

    def test_multiple_quantity_is_considered(self):
        product = Product.objects.create(
            name="Product",
            length=15,
            width=10,
            height=5,
            weight=2,
        )

        from .models import Order, OrderItem

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=3,
        )

        selected_box = find_suitable_box(order)

        self.assertIsNotNone(selected_box)


class OrderAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.product = Product.objects.create(
            name="Laptop",
            length=15,
            width=10,
            height=5,
            weight=2,
        )

        Box.objects.create(
            name="Small Box",
            internal_length=20,
            internal_width=20,
            internal_height=20,
            max_weight=5,
            cost=50,
        )

    def test_create_order_api(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product_id": self.product.id,
                        "quantity": 1,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            response.data["recommended_box"]["name"],
            "Small Box"
        )

    def test_invalid_quantity_is_rejected(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product_id": self.product.id,
                        "quantity": 0,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_nonexistent_product_is_rejected(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": [
                    {
                        "product_id": 9999,
                        "quantity": 1,
                    }
                ]
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        self.assertIn(
            "Product does not exist.",
            str(response.data)
        )

    def test_empty_items_are_rejected(self):
        response = self.client.post(
            "/api/orders/",
            {
                "items": []
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)

        self.assertIn(
            "At least one product is required.",
            str(response.data)
        )