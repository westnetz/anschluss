from django.core import mail
from django.urls import reverse


def test_form_sends_mail(client):
    response = client.post(
        reverse("order"), {"product_name": "Testname", "main_email": "foo@example.com"}
    )

    assert len(mail.outbox) == 1
    assert "foo@example.com" in mail.outbox[0].subject
