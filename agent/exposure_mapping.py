import json
from pathlib import Path

from agent.cases.registry import normalize_business_user


CONFIG_PATH = Path("config/business_users.json")


EXPOSURE_MAPPINGS = {
    "shipping_operator": [
        "route disruption",
        "port access",
        "fuel costs",
        "vessel security",
        "crew risk",
    ],
    "marine_insurer": [
        "war-risk exposure",
        "claims aggregation",
        "premium adequacy",
        "policy wording",
        "sanctions exclusions",
    ],
    "trade_finance_lender": [
        "sanctions exposure",
        "counterparty risk",
        "transaction documentation",
        "payment disruption",
        "collateral risk",
    ],
    "advanced_manufacturer": [
        "supplier concentration",
        "inventory runway",
        "production continuity",
        "input substitution difficulty",
        "customer delivery criticality",
    ],
    "infrastructure_contractor": [
        "public-sector bid pipeline",
        "contract award timing",
        "procurement delay",
        "payment risk",
        "contract repricing",
        "working-capital exposure",
        "board-level exposure reporting",
    ],
    "customer_facing_operator": [
        "digital trading interruption",
        "service downtime",
        "customer harm",
        "regulatory notification",
        "insurance claim readiness",
        "supplier / MSP dependency",
    ],
}


GENERIC_EXPOSURE_MAP = [
    "client exposure",
    "scenario planning",
    "mitigation options",
    "board-level communication",
    "market opportunity",
]


def _configured_business_user_ids():
    if not CONFIG_PATH.exists():
        return tuple(EXPOSURE_MAPPINGS)
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    ids = []
    for item in data.get("business_users", []):
        if isinstance(item, str):
            ids.append(normalize_business_user(item))
        elif item.get("id"):
            ids.append(normalize_business_user(item["id"]))
    return tuple(dict.fromkeys(ids))


VALID_BUSINESS_USERS = _configured_business_user_ids()


def get_exposure_map(business_user):
    canonical = normalize_business_user(business_user)
    return EXPOSURE_MAPPINGS.get(canonical, GENERIC_EXPOSURE_MAP)

