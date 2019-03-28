from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import EmailMessage
from django import forms
from django.template import loader
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

import yaml


class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in settings.ORDERFORM_FIELDS:
            self.fields[field["name"]] = getattr(forms, field["type"])(
                **field["kwargs"]
            )

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
    def context(self):
        return {"data": self.cleaned_data}

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
            reply_to=(self.cleaned_data[settings.ORDERFORM_FROM_EMAIL],),
            attachments=self.attachments,
        )
        order_message.send()
