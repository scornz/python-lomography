# Internal
from lomography.base import Lomography
from lomography.constants import BASE_URL

# External
from requests import HTTPError

# Typing
from typing import Optional


def get(lomo: Lomography, url: str, params: Optional[dict] = None):
    # If no parameters are provided, set it to an empty dictionary
    if params is None:
        params = {}

    try:
        res = lomo.session.get(
            f"{BASE_URL}{url}", params={**params, "api_key": lomo.api_key}
        )
        res.raise_for_status()
        # Return the JSON response
        return res.json()
    except HTTPError as e:
        raise e
