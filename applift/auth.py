# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from typing import Dict

from django.conf import settings


def get_headers() -> Dict[str, str]:
    """
    Returns bearer for applifting api
    :return:
    """
    return {"Bearer": settings.SECRET_TOKEN}
