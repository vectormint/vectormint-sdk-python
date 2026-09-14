# GENERATED FILE — DO NOT EDIT BY HAND.
# Source: https://api.vectormint.app/v1/openapi.json (OpenAPI 1.8.0).
# Regenerate with: python scripts/generate.py

from __future__ import annotations

import json
from typing import Any, Mapping, Sequence, TypeAlias
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

QueryScalar: TypeAlias = str | int | float | bool
QueryValue: TypeAlias = QueryScalar | Sequence[QueryScalar] | None


class VectorMintError(RuntimeError):
    def __init__(self, status: int, payload: Any):
        self.status = status
        self.payload = payload
        message = f"VectorMint request failed with HTTP {status}"
        if isinstance(payload, dict):
            error = payload.get("error")
            if isinstance(error, dict) and error.get("message"):
                message = str(error["message"])
        super().__init__(message)


class VectorMint:
    def __init__(
        self,
        api_key: str,
        *,
        auth_mode: str = "bearer",
        base_url: str = "https://api.vectormint.app/v1",
        timeout: float = 20.0,
    ):
        if not isinstance(api_key, str) or not api_key:
            raise ValueError("api_key is required")
        if auth_mode not in {"bearer", "x-api-key"}:
            raise ValueError("auth_mode must be 'bearer' or 'x-api-key'")
        self._api_key = api_key
        self._auth_mode = auth_mode
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def _request(
        self,
        method: str,
        route: str,
        *,
        path_params: Mapping[str, str],
        query: Mapping[str, QueryValue],
        body: Any = None,
    ) -> Any:
        rendered = route
        for name, value in path_params.items():
            rendered = rendered.replace("{" + name + "}", quote(str(value), safe=""))

        pairs: list[tuple[str, QueryScalar]] = []

        def query_scalar(value: QueryScalar) -> QueryScalar:
            return str(value).lower() if isinstance(value, bool) else value

        for name, value in query.items():
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                pairs.extend((name, query_scalar(item)) for item in value)
            else:
                pairs.append((name, query_scalar(value)))

        url = self._base_url + rendered
        if pairs:
            url += "?" + urlencode(pairs, doseq=True)

        headers = {"Accept": "application/json", "User-Agent": "vectormint-python/1.8.0"}
        if self._auth_mode == "x-api-key":
            headers["x-api-key"] = self._api_key
        else:
            headers["Authorization"] = f"Bearer {self._api_key}"

        encoded = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")

        request = Request(url, data=encoded, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self._timeout) as response:
                raw = response.read()
                return json.loads(raw.decode("utf-8")) if raw else None
        except HTTPError as exc:
            raw = exc.read()
            try:
                payload = json.loads(raw.decode("utf-8")) if raw else None
            except (UnicodeDecodeError, json.JSONDecodeError):
                payload = raw.decode("utf-8", errors="replace")
            raise VectorMintError(exc.code, payload) from exc

    def get_application_rules(self, **query: QueryValue) -> Any:
        return self._request("GET", "/application-rules", path_params={}, query=query, body=None)

    def list_cards(self, **query: QueryValue) -> Any:
        return self._request("GET", "/cards", path_params={}, query=query, body=None)

    def batch_cards(self, body: Any, **query: QueryValue) -> Any:
        return self._request("POST", "/cards/batch", path_params={}, query=query, body=body)

    def compare_cards(self, body: Any, **query: QueryValue) -> Any:
        return self._request("POST", "/cards/compare", path_params={}, query=query, body=body)

    def search_cards(self, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/search", path_params={}, query=query, body=None)

    def get_card(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}", path_params={"id": id}, query=query, body=None)

    def get_cards_id_assets(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/assets", path_params={"id": id}, query=query, body=None)

    def get_card_benefits(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/benefits", path_params={"id": id}, query=query, body=None)

    def get_card_credits(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/credits", path_params={"id": id}, query=query, body=None)

    def get_card_fees(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/fees", path_params={"id": id}, query=query, body=None)

    def get_card_freshness(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/freshness", path_params={"id": id}, query=query, body=None)

    def get_card_history(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/history", path_params={"id": id}, query=query, body=None)

    def get_card_offers(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/offers", path_params={"id": id}, query=query, body=None)

    def get_card_pricing(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/pricing", path_params={"id": id}, query=query, body=None)

    def get_card_provenance(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/provenance", path_params={"id": id}, query=query, body=None)

    def get_card_rewards(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/rewards", path_params={"id": id}, query=query, body=None)

    def get_cards_id_snapshot(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/cards/{id}/snapshot", path_params={"id": id}, query=query, body=None)

    def get_catalog_coverage(self, **query: QueryValue) -> Any:
        return self._request("GET", "/catalog/coverage", path_params={}, query=query, body=None)

    def get_catalog_export(self, **query: QueryValue) -> Any:
        return self._request("GET", "/catalog/export", path_params={}, query=query, body=None)

    def get_catalog_snapshot(self, **query: QueryValue) -> Any:
        return self._request("GET", "/catalog/snapshot", path_params={}, query=query, body=None)

    def get_catalog_sync(self, **query: QueryValue) -> Any:
        return self._request("GET", "/catalog/sync", path_params={}, query=query, body=None)

    def get_catalog_versions(self, **query: QueryValue) -> Any:
        return self._request("GET", "/catalog/versions", path_params={}, query=query, body=None)

    def get_categories(self, **query: QueryValue) -> Any:
        return self._request("GET", "/categories", path_params={}, query=query, body=None)

    def list_changes(self, **query: QueryValue) -> Any:
        return self._request("GET", "/changes", path_params={}, query=query, body=None)

    def list_notable_changes(self, **query: QueryValue) -> Any:
        return self._request("GET", "/changes/notable", path_params={}, query=query, body=None)

    def evaluate_transaction(self, body: Any, **query: QueryValue) -> Any:
        return self._request("POST", "/evaluate", path_params={}, query=query, body=body)

    def get_issuers(self, **query: QueryValue) -> Any:
        return self._request("GET", "/issuers", path_params={}, query=query, body=None)

    def get_offers_notable(self, **query: QueryValue) -> Any:
        return self._request("GET", "/offers/notable", path_params={}, query=query, body=None)

    def optimize_wallet(self, body: Any, **query: QueryValue) -> Any:
        return self._request("POST", "/optimize", path_params={}, query=query, body=body)

    def get_product_change_paths(self, **query: QueryValue) -> Any:
        return self._request("GET", "/product-change-paths", path_params={}, query=query, body=None)

    def get_reward_currencies(self, **query: QueryValue) -> Any:
        return self._request("GET", "/reward-currencies", path_params={}, query=query, body=None)

    def list_transfer_partners(self, **query: QueryValue) -> Any:
        return self._request("GET", "/transfer-partners", path_params={}, query=query, body=None)

    def list_webhooks(self, **query: QueryValue) -> Any:
        return self._request("GET", "/webhooks", path_params={}, query=query, body=None)

    def create_webhook(self, body: Any, **query: QueryValue) -> Any:
        return self._request("POST", "/webhooks", path_params={}, query=query, body=body)

    def get_webhook(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/webhooks/{id}", path_params={"id": id}, query=query, body=None)

    def update_webhook(self, id: str, body: Any, **query: QueryValue) -> Any:
        return self._request("PATCH", "/webhooks/{id}", path_params={"id": id}, query=query, body=body)

    def delete_webhook(self, id: str, **query: QueryValue) -> Any:
        return self._request("DELETE", "/webhooks/{id}", path_params={"id": id}, query=query, body=None)

    def list_webhook_deliveries(self, id: str, **query: QueryValue) -> Any:
        return self._request("GET", "/webhooks/{id}/deliveries", path_params={"id": id}, query=query, body=None)

    def test_webhook(self, id: str, **query: QueryValue) -> Any:
        return self._request("POST", "/webhooks/{id}/test", path_params={"id": id}, query=query, body=None)
