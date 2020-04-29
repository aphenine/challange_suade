import datetime

from django.db.models import Sum

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from shop.models import Order, OrderLine, VendorCommissions


class SummaryAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        date_string = request.query_params.get("date")
        print(date_string)

        # date = args[0]
        print(args)
        print(kwargs)
        # date = datetime.date(2019, 8, 2)
        date = datetime.datetime.strptime(date_string, '%Y%m%d').date()
        print(date)

        day_orders = Order.objects.filter(created_at__date=date)
        day_order_lines = OrderLine.objects.filter(order__created_at__date=date)

        distinct_customers = day_orders.values("customer_id").distinct().count()
        total_discount_amount = day_order_lines.aggregate(Sum("discounted_amount"))["discounted_amount__sum"]
        total_items = day_order_lines.aggregate(Sum("quantity"))["quantity__sum"]
        order_total_avg = day_order_lines.aggregate(Sum("total_amount"))["total_amount__sum"] / day_orders.count()
        discount_rate_avg = day_order_lines.aggregate(Sum("discount_rate"))["discount_rate__sum"] / day_orders.count()

        all_vendors = VendorCommissions.objects.all().values("vendor_id").distinct()
        total_commission = 0
        per_order_commission_avg = 0
        per_vendor_order_commissions = []
        for vendor in all_vendors:
            vendor_id = vendor["vendor_id"]
            vendor_orders = day_orders.filter(vendor_id=vendor_id)
            # Assume unique constraint
            vendor_commission = VendorCommissions.objects.get(date=date, vendor_id=vendor_id)

            for vendor_order in vendor_orders:
                order_total = vendor_order.products.through.objects.aggregate(Sum("total_amount")).get("total_amount__sum", 0)
                per_vendor_order_commissions.append(order_total * vendor_commission.rate)
                total_commission += order_total * vendor_commission.rate

        if len(per_vendor_order_commissions) > 0:
            per_order_commission_avg = sum(per_vendor_order_commissions) / len(per_vendor_order_commissions)

        return Response({
            "customers": distinct_customers,
            "total_discount_amount": total_discount_amount,
            "items": total_items,
            "order_total_avg": order_total_avg,
            "discount_rate_avg": discount_rate_avg,
            "commissions": {
                "total": total_commission,
                "order_average": per_order_commission_avg,
            }
        })
