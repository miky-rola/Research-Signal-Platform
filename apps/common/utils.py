import base64
import json
import logging

import pyotp
from django.contrib.auth import get_user_model
from django.db.models import F
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from rest_framework.filters import OrderingFilter

User = get_user_model()


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


class CustomOrderingFilter(OrderingFilter):
    """Custom OrderingFilter with fields for description"""

    def get_schema_fields(self, view):
        check = hasattr(view, "ordering_fields")

        if check:
            fields = [f"`{field}`" for field in view.ordering_fields]
            reverse_fields = [f"`-{field}`" for field in view.ordering_fields]

            self.ordering_description = (
                f"Fields to use when ordering the results: {', '.join(fields)}. "
                f"The client may also specify reverse orderings by prefixing the field name "
                f"with `-`: {', '.join(reverse_fields)}."
            )

        return super().get_schema_fields(view)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:

            def order_by_field(field):
                if field.startswith("-"):
                    return F(field[1:]).desc(nulls_last=True)
                else:
                    return F(field).asc(nulls_last=True)

            return queryset.order_by(*[order_by_field(field) for field in ordering])

        return queryset


class OTPUtils:
    @classmethod
    def generate_token(cls, data):
        data = json.dumps(data)
        encoded = base64.b32encode(data.encode())
        return encoded.decode()

    @classmethod
    def generate_otp(cls, user: User, life=600):
        secret = pyotp.random_base32()
        data = {"user_id": str(user.id), "secret": secret}
        # generate token
        token = cls.generate_token(data)

        totp = pyotp.TOTP(secret, interval=life)
        return totp.now(), token

    @classmethod
    def decode_token(cls, token: str):
        token = token.encode()
        decoded = base64.b32decode(token)
        decoded = decoded.decode()
        try:
            data = json.loads(decoded)
        except Exception as e:
            logging.warning(e)
            return None
        return data

    @classmethod
    def verify_otp(cls, code, secret, life=600):
        totp = pyotp.TOTP(secret, interval=life)
        return totp.verify(code)
