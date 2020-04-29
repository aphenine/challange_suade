import datetime

from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Order, OrderLine


class SummaryAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        # date = args[0]
        date = datetime.date(2020, 1, 1)

        distinct_customers = Order.objects.filter(created_at=date).values("customer_id").distinct().count()
        total_discount_amount = 0  # Not sure how to calculate this yet
        total_items = OrderLine.objects.filter(order__created_at=date).aggregate(Sum("quantity"))
        # order_total_avg = Order.objects.filter(created_at=date).orderline_set.aggregate(Sum("total_amount")) / OrderLine.objects.filter(created_at=date).count()
        # discount_rate_avg = OrderLine.objects.filter(order__created_at=date).aggregate(Sum("discount_rate")) / OrderLine.objects.filter(order__created_at=date).count()

        return Response({
            "customers": distinct_customers,
            "total_discount_amount": total_discount_amount,
            "items": total_items,
            # "order_total_avg": order_total_avg,
            # "discount_rate_avg": discount_rate_avg,
        })
