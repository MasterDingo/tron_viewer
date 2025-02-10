# config.py
import os
from typing import Any

from dotenv import load_dotenv

from tronpy.providers import HTTPProvider


load_dotenv()


class Settings:
    tron_network: str = os.getenv("TRON_NETWORK", "")
    tron_timeout: str = os.getenv("TRON_TIMEOUT", "")
    tron_api_key: str = os.getenv("TRON_API_KEY", "")
    database_url: str = os.getenv("DATABASE_URL", "")

    def get_tron_params(self) -> dict[str, Any]:
        params = {}

        if self.tron_network:
            if (
                self.tron_network.startswith("http://")
                or self.tron_network.startswith("https://")
                or self.tron_api_key
            ):
                provider_params = {}
                if self.tron_network:
                    provider_params["network"] = self.tron_network
                if self.tron_api_key:
                    provider_params["api_key"] = self.tron_api_key
                params["provider"] = HTTPProvider(**provider_params)
            else:
                params["network"] = self.tron_network

        if self.tron_timeout:
            try:
                params["conf"] = {"timeout": float(self.tron_timeout)}
            except ValueError:
                raise ValueError(f"Invalid timeout value: {self.tron_timeout}")

        return params


settings = Settings()
