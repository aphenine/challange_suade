import datetime
import json

from django.test import Client, TestCase

from shop.models import Order, Product, OrderLine


class SummaryAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_items(self):
        created = datetime.datetime(2020, 10, 1, 1, 2, 44)
        order = Order.objects.create(
            id=1000,
            created_at=created,
            vendor_id=1,
            customer_id=1,
        )
        print(order.pk)

        product = Product.objects.create(
            id=1000,
            description="Blah, blah, blah",
        )
        print(product.pk)

        order_line = OrderLine.objects.create(
            id=1,
            order=order,
            product=product,
            product_description="Blah",
            product_price=0,
            product_vat_rate=0,
            discount_rate=0,
            quantity=4,
            full_price_amount=0,
            discounted_amount=0,
            vat_amount=0,
            total_amount=0,
        )

        resp = self.client.get("/shop/summary/?date=20201001")

        data = json.loads(resp.content.decode('utf-8'))

        print(data)

        assert data == {
            'customers': 1,
            'total_discount_amount': 0.0,
            'items': 4,
            'order_total_avg': 0.0,
            'discount_rate_avg': 0.0,
            'commissions': {'total': 0, 'order_average': 0}
        }
