# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Dict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_headers() -> Dict[str, str]:
    """
    Returns bearer for applifting api
    :return:
    """

    try:
        return {"Bearer": settings.SECRET_TOKEN}
    except ImproperlyConfigured:
        raise ImproperlyConfigured("SECRET_TOKEN is not set")
