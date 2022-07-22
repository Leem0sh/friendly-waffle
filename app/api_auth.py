# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest
from django.utils.crypto import constant_time_compare
from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        return constant_time_compare(token, settings.NINJA_BEARER_TOKEN)
