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
    "importer_exporter": [
        "lead times",
        "freight rates",
        "inventory risk",
        "supplier concentration",
        "customs disruption",
    ],
    "trade_finance_lender": [
        "sanctions exposure",
        "counterparty risk",
        "cargo documentation",
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
    "UK infrastructure contractor": [
        "public-sector bid pipeline",
        "contract award timing",
        "procurement delay",
        "payment risk",
        "contract repricing",
        "working-capital exposure",
        "board-level exposure reporting",
    ],
    "UK infrastructure contractor bidding for government-funded transport and energy projects": [
        "public-sector bid pipeline",
        "transport and energy project award timing",
        "procurement delay",
        "project-delay contingency planning",
        "payment risk",
        "contract repricing",
        "working-capital stress testing",
        "board-level exposure reporting",
    ],
    "uk_infrastructure_contractor": [
        "public-sector bid pipeline",
        "contract award timing",
        "procurement delay",
        "payment risk",
        "contract repricing",
        "working-capital exposure",
    ],
    "infrastructure_contractor": [
        "public-sector bid pipeline",
        "contract award timing",
        "procurement delay",
        "payment risk",
        "contract repricing",
        "working-capital exposure",
    ],
    "consultant": [
        "client exposure",
        "scenario planning",
        "mitigation options",
        "board-level communication",
        "market opportunity",
    ],
}

VALID_BUSINESS_USERS = tuple(EXPOSURE_MAPPINGS.keys())


def get_exposure_map(business_user):
    if business_user not in EXPOSURE_MAPPINGS:
        raise ValueError(f"Unsupported business user: {business_user}")

    return EXPOSURE_MAPPINGS[business_user]
