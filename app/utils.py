from os import _Environ
from typing import Any

from tronpy.providers import HTTPProvider


def make_tron_params(env: _Environ[str] | dict[str, str]) -> dict[str, Any]:
    params = {}
    network = env.get("TRON_NETWORK", "")
    timeout = env.get("TRON_TIMEOUT", "")
    api_key = env.get("TRON_API_KEY", "")

    if network:
        if network.startswith("http://") or network.startswith("https://") or api_key:
            provider_params = {}
            if network:
                provider_params["network"] = network
            if api_key:
                provider_params["api_key"] = api_key
            params["provider"] = HTTPProvider(**provider_params)
        else:
            params["network"] = network

    if timeout:
        params["conf"] = {"timeout": float(timeout)}

    return params
