from pathlib import Path

from django.core.management.base import BaseCommand
import csv

from django.db import transaction

from shop.models import Product, Order, OrderLine, ProductPromotion, Promotion, VendorCommissions


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument(
            "-d", "--data",
            type=str,
            required=True,
            dest="data_dir",
            help="Please enter the data directory from which the data import will happen."
        )

    def handle(self, *args, **options):
        data_dir = Path(options["data_dir"])

        # Prevent writing into the DB unless the entire operation succeeds.
        with transaction.atomic():
            # Import stand-alone entities first
            with open(data_dir / "products.csv") as csvfile:
                products_reader = csv.DictReader(csvfile)
                for row in products_reader:
                    Product.objects.create(
                        id=row["id"],
                        description=row["description"],
                    )

            with open(data_dir / "orders.csv") as csvfile:
                products_reader = csv.DictReader(csvfile)
                for row in products_reader:
                    Order.objects.create(
                        id=row["id"],
                        created_at=row["created_at"],
                        vendor_id=row["vendor_id"],
                        customer_id=row["customer_id"],
                    )

            with open(data_dir / "promotions.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Promotion.objects.create(
                        id=row["id"],
                        description=row["description"],
                    )

            with open(data_dir / "commissions.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    VendorCommissions.objects.create(
                        # id=row[0],
                        date=row["date"],
                        vendor_id=row["vendor_id"],
                        rate=row["rate"],
                    )

            # Now the link tables
            with open(data_dir / "order_lines.csv") as csvfile:
                products_reader = csv.DictReader(csvfile)
                for row in products_reader:
                    OrderLine.objects.create(
                        # id=row[0],
                        order_id=row["order_id"],
                        product_id=row["product_id"],
                        product_description=row["product_description"],
                        product_price=row["product_price"],
                        product_vat_rate=row["product_vat_rate"],
                        discount_rate=row["discount_rate"],
                        quantity=row["quantity"],
                        full_price_amount=row["full_price_amount"],
                        discounted_amount=row["discounted_amount"],
                        vat_amount=row["vat_amount"],
                        total_amount=row["total_amount"],
                    )

            with open(data_dir / "product_promotions.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    ProductPromotion.objects.create(
                        # id=row[0],
                        date=row["date"],
                        product_id=row["product_id"],
                        promotion_id=row["promotion_id"],
                    )

