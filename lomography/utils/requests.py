from __future__ import annotations

# Internal
from lomography.constants import BASE_URL

# Typing
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography

# External
from aiohttp import ClientError


async def get(lomo: Lomography, url: str, params: Optional[dict] = None):
    # If no parameters are provided, set it to an empty dictionary
    if params is None:
        params = {}

    try:
        async with lomo.session.get(
            f"{BASE_URL}{url}", params={**params, "api_key": lomo.api_key}
        ) as response:
            response.raise_for_status()
            return await response.json()
    except ClientError as e:
        raise e
