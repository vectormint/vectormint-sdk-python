# VectorMint Python SDK

Official dependency-free Python 3.10+ SDK for the VectorMint REST API. The client is generated from VectorMint's canonical OpenAPI contract, is MIT licensed, and contains no license or tier gating. API quotas and endpoint entitlements are enforced server-side.

## Install

```bash
pip install git+https://github.com/vectormint/vectormint-sdk-python
```

**PyPI publication is still pending.** Until `vectormint` is published to PyPI, install directly from this GitHub repository using the command above.

## 5-line quickstart

```python
import os
from vectormint import VectorMint
vm = VectorMint(api_key=os.environ["VECTORMINT_API_KEY"])
result = vm.search_cards(q="chase", limit=5)
print(result["data"])
```

Use `auth_mode="x-api-key"` if you prefer the `x-api-key` header.

## Coverage

The generated client covers card list/search/get/batch/compare; offers, rewards, credits, fees, benefits, pricing, provenance, freshness, assets and history/snapshots; catalog sync/export/coverage; evaluate and optimize; issuers, categories, reward currencies, transfer partners, application rules, product-change paths, notable offers and changes; and webhook CRUD, deliveries and test calls.

## Regeneration

```bash
python scripts/generate.py
```

Generation reads `https://api.vectormint.app/v1/openapi.json`. CI regenerates on every push and pull request and fails if `src/vectormint/client.py` drifts from the OpenAPI contract.

## License

MIT © 2026 VectorMint
