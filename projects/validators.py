import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

GITHUB_HOST = "github.com"

RU_PHONE_PREFIX = "+7"
ALT_RU_PHONE_PREFIX = "8"
PHONE_LEN_PLUS_PREFIX = 12
PHONE_LEN_ALT_PREFIX = 11


def github_url_validator(value: str):
    if not value:
        return
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    if GITHUB_HOST not in host:
        raise ValidationError("Ссылка должна вести на GitHub.", code="invalid_github")


def normalize_phone_digits(value: str) -> str:
    """Приводит номер к формату +7XXXXXXXXXX для хранения и сравнения уникальности."""
    v = value.strip()
    if v.startswith(RU_PHONE_PREFIX) and len(v) == PHONE_LEN_PLUS_PREFIX:
        return v
    if v.startswith(ALT_RU_PHONE_PREFIX) and len(v) == PHONE_LEN_ALT_PREFIX:
        return RU_PHONE_PREFIX + v[1:]
    return v
