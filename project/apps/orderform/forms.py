from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.signing import dumps
from django.forms import Form, CharField, EmailField
from django.template import loader
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

import yaml


class OrderForm(Form):
    product_name = CharField(label=_("Product Name"))
    main_email = EmailField(label=_("E-Mail Address"))

    SALT = "orderform"

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    @property
    def yaml_filename(self):
        return now().strftime("order-%Y-%m-%dT%H-%M-%S.yaml")

    @property
    def yaml(self):
        rv = MIMEText(
            yaml.safe_dump(self.cleaned_data, default_flow_style=False, indent=4),
            "yaml",
        )
        rv.add_header("Content-Disposition", "attachment", filename=self.yaml_filename)
        return rv

    @property
    def attachments(self):
        return [self.yaml]

    @property
    def redo_url(self):
        url = reverse(
            "order_prefilled", args=(dumps(self.data, compress=True, salt=self.SALT),)
        )
        if self.request:
            url = self.request.build_absolute_uri(url)
        return url

    @property
    def context(self):
        return {"data": self.cleaned_data, "redo_url": self.redo_url}

    @property
    def body(self):
        return loader.render_to_string(
            "orderform/order_mail_body.txt", self.context
        ).strip()

    @property
    def subject(self):
        return loader.render_to_string(
            "orderform/order_mail_subject.txt", self.context
        ).strip()

    def save(self):
        print("Saving form!")
        order_message = EmailMessage(
            subject=self.subject,
            body=self.body,
            to=[address for _, address in settings.ADMINS],
            reply_to=(self.cleaned_data["main_email"],),
            attachments=self.attachments,
        )
        order_message.send()
