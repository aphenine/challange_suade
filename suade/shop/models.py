from django.db import models

# Create your models here.


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()
    products = models.ManyToManyField("Product", through="OrderLine")


class OrderLine(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    product_description = models.CharField(max_length=255)
    product_price = models.FloatField()
    product_vat_rate = models.FloatField()
    discount_rate = models.FloatField()
    quantity = models.IntegerField()
    full_price_amount = models.FloatField()
    discounted_amount = models.FloatField()
    vat_amount = models.FloatField()
    total_amount = models.FloatField()


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    orders = models.ManyToManyField("Order", through="OrderLine")
    promotions = models.ManyToManyField("Promotion", through="ProductPromotion")


class Promotion(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    products = models.ManyToManyField("Product", through="ProductPromotion")


class ProductPromotion(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    promotion = models.ForeignKey("Promotion", on_delete=models.CASCADE)


class VendorCommissions(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    vendor_id = models.IntegerField()   # This seems to be a Foreign key to data we don't have
    rate = models.FloatField()
