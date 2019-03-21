from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import OrderForm


class OrderCompleteView(TemplateView):
    template_name = "orderform/order_complete.html"


class OrderView(FormView):
    form_class = OrderForm
    template_name = "orderform/order.html"
    success_url = reverse_lazy("order_complete")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
