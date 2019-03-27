from django.urls import path

from .views import OrderCompleteView, OrderView

urlpatterns = [
    path("", OrderView.as_view(), name="order"),
    path("prefill/<data>/", OrderView.as_view(), name="order_prefilled"),
    path("success/", OrderCompleteView.as_view(), name="order_complete"),
]
