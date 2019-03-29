from django.core import mail
from django.urls import reverse

from ..forms import OrderForm


def test_form_sends_mail(client):
    response = client.post(
        reverse("order"), {"product_name": "Testname", "main_email": "foo@example.com"}
    )

    assert len(mail.outbox) == 1  # nosec
    assert "foo@example.com" in mail.outbox[0].subject  # nosec


def test_redo_url(client):
    """
    Generate a redo url with one field filled.
    Verify the field will be prefilled when loading the redo_url for this form.
    """
    redo_url = OrderForm(request=None, data={"product_name": "Test Product"}).redo_url
    response = client.get(redo_url)

    assert b"Test Product" in response.content  # nosec
