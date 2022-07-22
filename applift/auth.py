# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Tuple

from django.conf import settings


def get_bearer() -> Tuple[str, str]:
    """
    Returns bearer for applifting api
    :return:
    """
    return "Authorization", f"Bearer: {settings.SECRET_TOKEN}"
