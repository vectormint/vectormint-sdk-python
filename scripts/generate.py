#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

SPEC_URL = os.environ.get("VECTORMINT_OPENAPI_URL", "https://api.vectormint.app/v1/openapi.json")
SPEC_FILE = os.environ.get("VECTORMINT_OPENAPI_FILE", "")
OUTPUT = Path("src/vectormint/client.py")
METHODS = ("get", "post", "put", "patch", "delete")
FRIENDLY_NAMES = {'get /cards': ('listCards', 'list_cards'), 'get /cards/search': ('searchCards', 'search_cards'), 'post /cards/batch': ('batchCards', 'batch_cards'), 'post /cards/compare': ('compareCards', 'compare_cards'), 'get /cards/{id}': ('getCard', 'get_card'), 'get /cards/{id}/offers': ('getCardOffers', 'get_card_offers'), 'get /cards/{id}/rewards': ('getCardRewards', 'get_card_rewards'), 'get /cards/{id}/credits': ('getCardCredits', 'get_card_credits'), 'get /cards/{id}/fees': ('getCardFees', 'get_card_fees'), 'get /cards/{id}/benefits': ('getCardBenefits', 'get_card_benefits'), 'get /cards/{id}/provenance': ('getCardProvenance', 'get_card_provenance'), 'get /cards/{id}/history': ('getCardHistory', 'get_card_history'), 'get /cards/{id}/pricing': ('getCardPricing', 'get_card_pricing'), 'get /cards/{id}/freshness': ('getCardFreshness', 'get_card_freshness'), 'get /cards/{id}/assets': ('getCardsIdAssets', 'get_cards_id_assets'), 'get /cards/{id}/snapshot': ('getCardsIdSnapshot', 'get_cards_id_snapshot'), 'get /catalog/snapshot': ('getCatalogSnapshot', 'get_catalog_snapshot'), 'get /catalog/sync': ('getCatalogSync', 'get_catalog_sync'), 'get /catalog/export': ('getCatalogExport', 'get_catalog_export'), 'get /catalog/versions': ('getCatalogVersions', 'get_catalog_versions'), 'get /catalog/coverage': ('getCatalogCoverage', 'get_catalog_coverage'), 'post /evaluate': ('evaluateTransaction', 'evaluate_transaction'), 'post /optimize': ('optimizeWallet', 'optimize_wallet'), 'get /issuers': ('getIssuers', 'get_issuers'), 'get /categories': ('getCategories', 'get_categories'), 'get /reward-currencies': ('getRewardCurrencies', 'get_reward_currencies'), 'get /transfer-partners': ('listTransferPartners', 'list_transfer_partners'), 'get /application-rules': ('getApplicationRules', 'get_application_rules'), 'get /product-change-paths': ('getProductChangePaths', 'get_product_change_paths'), 'get /offers/notable': ('getOffersNotable', 'get_offers_notable'), 'get /changes': ('listChanges', 'list_changes'), 'get /changes/notable': ('listNotableChanges', 'list_notable_changes'), 'get /webhooks': ('listWebhooks', 'list_webhooks'), 'post /webhooks': ('createWebhook', 'create_webhook'), 'get /webhooks/{id}': ('getWebhook', 'get_webhook'), 'patch /webhooks/{id}': ('updateWebhook', 'update_webhook'), 'delete /webhooks/{id}': ('deleteWebhook', 'delete_webhook'), 'get /webhooks/{id}/deliveries': ('listWebhookDeliveries', 'list_webhook_deliveries'), 'post /webhooks/{id}/test': ('testWebhook', 'test_webhook')}
HEADER = '# GENERATED FILE — DO NOT EDIT BY HAND.\n# Source: https://api.vectormint.app/v1/openapi.json (OpenAPI 1.8.0).\n# Regenerate with: python scripts/generate.py\n\nfrom __future__ import annotations\n\nimport json\nfrom typing import Any, Mapping, Sequence, TypeAlias\nfrom urllib.error import HTTPError\nfrom urllib.parse import quote, urlencode\nfrom urllib.request import Request, urlopen\n\nQueryScalar: TypeAlias = str | int | float | bool\nQueryValue: TypeAlias = QueryScalar | Sequence[QueryScalar] | None\n\n\nclass VectorMintError(RuntimeError):\n    def __init__(self, status: int, payload: Any):\n        self.status = status\n        self.payload = payload\n        message = f"VectorMint request failed with HTTP {status}"\n        if isinstance(payload, dict):\n            error = payload.get("error")\n            if isinstance(error, dict) and error.get("message"):\n                message = str(error["message"])\n        super().__init__(message)\n\n\nclass VectorMint:\n    def __init__(\n        self,\n        api_key: str,\n        *,\n        auth_mode: str = "bearer",\n        base_url: str = "https://api.vectormint.app/v1",\n        timeout: float = 20.0,\n    ):\n        if not isinstance(api_key, str) or not api_key:\n            raise ValueError("api_key is required")\n        if auth_mode not in {"bearer", "x-api-key"}:\n            raise ValueError("auth_mode must be \'bearer\' or \'x-api-key\'")\n        self._api_key = api_key\n        self._auth_mode = auth_mode\n        self._base_url = base_url.rstrip("/")\n        self._timeout = timeout\n\n    def _request(\n        self,\n        method: str,\n        route: str,\n        *,\n        path_params: Mapping[str, str],\n        query: Mapping[str, QueryValue],\n        body: Any = None,\n    ) -> Any:\n        rendered = route\n        for name, value in path_params.items():\n            rendered = rendered.replace("{" + name + "}", quote(str(value), safe=""))\n\n        pairs: list[tuple[str, QueryScalar]] = []\n\n        def query_scalar(value: QueryScalar) -> QueryScalar:\n            return str(value).lower() if isinstance(value, bool) else value\n\n        for name, value in query.items():\n            if value is None:\n                continue\n            if isinstance(value, (list, tuple)):\n                pairs.extend((name, query_scalar(item)) for item in value)\n            else:\n                pairs.append((name, query_scalar(value)))\n\n        url = self._base_url + rendered\n        if pairs:\n            url += "?" + urlencode(pairs, doseq=True)\n\n        headers = {"Accept": "application/json"}\n        if self._auth_mode == "x-api-key":\n            headers["x-api-key"] = self._api_key\n        else:\n            headers["Authorization"] = f"Bearer {self._api_key}"\n\n        encoded = None\n        if body is not None:\n            headers["Content-Type"] = "application/json"\n            encoded = json.dumps(body, separators=(",", ":")).encode("utf-8")\n\n        request = Request(url, data=encoded, headers=headers, method=method)\n        try:\n            with urlopen(request, timeout=self._timeout) as response:\n                raw = response.read()\n                return json.loads(raw.decode("utf-8")) if raw else None\n        except HTTPError as exc:\n            raw = exc.read()\n            try:\n                payload = json.loads(raw.decode("utf-8")) if raw else None\n            except (UnicodeDecodeError, json.JSONDecodeError):\n                payload = raw.decode("utf-8", errors="replace")\n            raise VectorMintError(exc.code, payload) from exc\n\n'

def resolve_ref(spec: dict[str, Any], value: Any) -> Any:
    if not isinstance(value, dict) or "$ref" not in value:
        return value
    ref = str(value["$ref"])
    if not ref.startswith("#/"):
        raise RuntimeError(f"Only local OpenAPI refs are supported: {ref}")
    cursor: Any = spec
    for token in ref[2:].split("/"):
        cursor = cursor[token.replace("~1", "/").replace("~0", "~")]
    return cursor

def has_api_key_security(spec: dict[str, Any], operation: dict[str, Any]) -> bool:
    security = operation.get("security", spec.get("security", []))
    return any("BearerAuth" in item or "ApiKeyHeader" in item for item in security)

def words(value: str) -> list[str]:
    return [p.lower() for p in re.split(r"[^A-Za-z0-9]+", value.replace("{", " ").replace("}", " ")) if p]

def pascal(parts: list[str]) -> str:
    return "".join(p[:1].upper() + p[1:] for p in parts)

def default_names(method: str, route: str) -> tuple[str, str]:
    route_words = words(route)
    return method + pascal(route_words), method + "_" + "_".join(route_words)

def safe_identifier(value: str) -> str:
    candidate = re.sub(r"[^A-Za-z0-9_]", "_", value)
    return candidate if re.match(r"^[A-Za-z_]", candidate) else "_" + candidate

def collect_operations(spec: dict[str, Any]) -> list[dict[str, Any]]:
    operations: list[dict[str, Any]] = []
    used_py: set[str] = set()
    for route in sorted(spec.get("paths", {})):
        item = spec["paths"][route]
        for method in METHODS:
            operation = resolve_ref(spec, item.get(method))
            if not isinstance(operation, dict) or not has_api_key_security(spec, operation):
                continue
            key = f"{method} {route}"
            _, py_name = FRIENDLY_NAMES.get(key, default_names(method, route))
            if py_name in used_py:
                py_name += "_" + method
            used_py.add(py_name)
            parameters = [resolve_ref(spec, p) for p in [*item.get("parameters", []), *operation.get("parameters", [])]]
            path_params = [str(p["name"]) for p in parameters if isinstance(p, dict) and p.get("in") == "path" and p.get("name")]
            for placeholder in re.findall(r"\{([^}]+)\}", route):
                if placeholder not in path_params:
                    path_params.append(placeholder)
            operations.append({
                "method": method,
                "path": route,
                "py_name": py_name,
                "path_params": path_params,
                "has_body": bool(resolve_ref(spec, operation.get("requestBody"))),
            })
    return operations

def py_method(operation: dict[str, Any]) -> str:
    args = [f"{safe_identifier(name)}: str" for name in operation["path_params"]]
    if operation["has_body"]:
        args.append("body: Any")
    args.append("**query: QueryValue")
    if operation["path_params"]:
        path_object = "{" + ", ".join(f"{json.dumps(name)}: {safe_identifier(name)}" for name in operation["path_params"]) + "}"
    else:
        path_object = "{}"
    body = "body" if operation["has_body"] else "None"
    return (
        f"    def {operation['py_name']}(self, {', '.join(args)}) -> Any:\n"
        f"        return self._request({json.dumps(operation['method'].upper())}, {json.dumps(operation['path'])}, "
        f"path_params={path_object}, query=query, body={body})"
    )

def load_spec() -> dict[str, Any]:
    if SPEC_FILE:
        return json.loads(Path(SPEC_FILE).read_text())
    req = Request(SPEC_URL, headers={"Accept": "application/json", "User-Agent": "VectorMint-Python-SDK-Generator/1.8"})
    with urlopen(req, timeout=30) as response:
        return json.load(response)

spec = load_spec()
operations = collect_operations(spec)
if not operations:
    raise RuntimeError("No API-key-authenticated OpenAPI operations were found.")
version = str(spec.get("info", {}).get("version", "unknown"))
header = HEADER.replace("OpenAPI 1.8.0", f"OpenAPI {version}")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(header + "\n\n".join(py_method(op) for op in operations) + "\n")
print(f"Generated {len(operations)} Python SDK operations from OpenAPI {version}.")
