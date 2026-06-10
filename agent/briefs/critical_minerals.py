from agent.briefs import legacy


def generate(evidence_pack):
    return legacy.generate_brief(
        topic=evidence_pack["topic"],
        business_user=evidence_pack["business_user"],
        region=evidence_pack["region"],
        time_horizon=evidence_pack["time_horizon"],
        concerns=evidence_pack.get("concerns", []),
        sources=evidence_pack.get("evidence", []),
        evidence_pack=evidence_pack,
    )

