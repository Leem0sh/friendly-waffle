# -*- encoding: utf-8 -*-
# ! python3

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%d.%m.%Y %H:%M:%S",
        format="[%(asctime)s] %(levelname)s [%(name)s:%(module)s %(funcName)s:%(lineno)s] %(message)s",
    )
