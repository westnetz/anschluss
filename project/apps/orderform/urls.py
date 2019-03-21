from django.urls import path

from .views import OrderCompleteView, OrderView

urlpatterns = [
    path("", OrderView.as_view(), name="order"),
    path("success/", OrderCompleteView.as_view(), name="order_complete"),
]
