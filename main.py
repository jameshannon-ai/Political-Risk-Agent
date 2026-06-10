from pathlib import Path
import argparse

from agent.brief_generator import generate_brief, save_brief
from agent.core.workflow import EXPERIMENTAL_GENERIC_WARNING, run_topic_workflow
from agent.evidence_pack_builder import build_evidence_pack, save_evidence_pack
from agent.exposure_mapping import VALID_BUSINESS_USERS
from agent.live_search import run_live_searches
from agent.source_fetcher import fetch_selected_sources
from agent.source_audit import generate_source_audit, save_source_audit
from agent.source_parser import parse_source_notes
from agent.source_ranker import rank_candidate_sources
from agent.source_strategy import SOURCE_CATEGORIES, create_source_strategy

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


def parse_concerns(raw_concerns):
    return [concern.strip() for concern in raw_concerns.split(",") if concern.strip()]


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Political Risk Agent")
    subparsers = parser.add_subparsers(dest="command")

    run_topic = subparsers.add_parser("run-topic", help="Generate artefacts for a fresh topic.")
    run_topic.add_argument("--topic", required=True)
    run_topic.add_argument("--business-user", required=True)
    run_topic.add_argument("--decision-context", default="")
    run_topic.add_argument("--domain", default=None)
    run_topic.add_argument("--region", default="")
    run_topic.add_argument("--time-horizon", default="")
    run_topic.add_argument("--concerns", default="")
    run_topic.add_argument("--output-dir", default="outputs")
    run_topic.add_argument("--source-notes-file", default="")
    run_topic.add_argument("--live", action="store_true", help="Use live retrieval deliberately. Default is manual/offline input.")
    return parser


def run_topic_command(args):
    print(EXPERIMENTAL_GENERIC_WARNING)
    source_notes = ""
    if args.source_notes_file:
        source_notes = Path(args.source_notes_file).read_text(encoding="utf-8")
    result = run_topic_workflow(
        topic=args.topic,
        business_user=args.business_user,
        decision_context=args.decision_context,
        region=args.region,
        time_horizon=args.time_horizon,
        concerns=parse_concerns(args.concerns),
        domain=args.domain,
        output_dir=args.output_dir,
        source_notes=source_notes,
        live=args.live,
    )
    print(f"Evidence pack saved to: {result['evidence_pack_path']}")
    print(f"Source audit saved to: {result['source_audit_path']}")
    print(f"Brief saved to: {result['brief_path']}")


def prompt_for_business_user():
    print("Available business users:")
    for user in VALID_BUSINESS_USERS:
        print(f"- {user}")

    while True:
        business_user = input("Business user: ").strip()
        if business_user in VALID_BUSINESS_USERS:
            return business_user

        print("Invalid business user. Please enter one of the listed values.")


def prompt_for_source_notes():
    print("\nPaste source notes. Enter END on its own line when finished.")
    print("Leave empty and enter END if you do not have sources yet.")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def prompt_for_mode():
    print("Choose source mode:")
    print("1. manual_source_mode")
    print("2. live_search_mode")
    while True:
        choice = input("Mode: ").strip()
        if choice in {"1", "manual_source_mode"}:
            return "manual_source_mode"
        if choice in {"2", "live_search_mode"}:
            return "live_search_mode"
        print("Please choose 1 or 2.")


def prompt_for_case_inputs():
    topic = input("Topic: ").strip()
    business_user = prompt_for_business_user()
    region = input("Region: ").strip()
    time_horizon = input("Time horizon: ").strip()
    concerns = parse_concerns(input("Concerns, comma-separated: "))
    return topic, business_user, region, time_horizon, concerns


def run_manual_source_mode(output_dir):
    topic, business_user, region, time_horizon, concerns = prompt_for_case_inputs()
    source_notes = prompt_for_source_notes()
    sources = parse_source_notes(source_notes) if source_notes else []

    brief = generate_brief(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        sources=sources,
    )

    output_path = save_brief(brief, output_dir)
    print(f"\nBrief saved to: {output_path}")


def run_live_search_mode(output_dir):
    topic, business_user, region, time_horizon, concerns = prompt_for_case_inputs()

    print("\nCreating source strategy...")
    source_strategy = create_source_strategy(
        topic,
        region,
        time_horizon,
        business_user=business_user,
        concerns=concerns,
    )

    print("Running searches...")
    search_result = run_live_searches(source_strategy)
    if search_result["fallback_demo_data_used"]:
        print("No search API key detected. Using curated local source pack.")

    print("Ranking candidate sources...")
    ranking_result = rank_candidate_sources(
        search_result["candidate_sources"],
        topic=topic,
        categories=SOURCE_CATEGORIES,
        per_category=1,
    )
    selected_sources = ranking_result["selected_sources"]
    rejected_sources = ranking_result["rejected_sources"]

    print("Fetching selected sources and extracting evidence...")
    fetched_result = fetch_selected_sources(
        selected_sources,
        fallback_demo_data_used=search_result["fallback_demo_data_used"],
    )
    evidence_pack = build_evidence_pack(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        source_strategy=source_strategy,
        search_result=search_result,
        selected_sources=selected_sources,
        rejected_sources=rejected_sources,
        fetched_result=fetched_result,
    )
    evidence_pack["duplicate_urls_removed"] = ranking_result["duplicate_urls_removed"]

    evidence_pack_path = save_evidence_pack(evidence_pack, output_dir)
    source_audit = generate_source_audit(evidence_pack)
    source_audit_path = save_source_audit(source_audit, output_dir, topic)
    brief = generate_brief(
        topic=topic,
        business_user=business_user,
        region=region,
        time_horizon=time_horizon,
        concerns=concerns,
        sources=evidence_pack["evidence"],
        evidence_pack=evidence_pack,
    )
    brief_path = save_brief(brief, output_dir)

    print(f"\nEvidence pack saved to: {evidence_pack_path}")
    print(f"Source audit saved to: {source_audit_path}")
    print(f"Brief saved to: {brief_path}")


def main():
    if load_dotenv:
        load_dotenv()

    parser = build_arg_parser()
    args = parser.parse_args()
    if args.command == "run-topic":
        run_topic_command(args)
        return

    print("Marine & Trade Risk Agent")
    print("-------------------------")
    mode = prompt_for_mode()
    output_dir = Path("outputs")

    if mode == "live_search_mode":
        run_live_search_mode(output_dir)
    else:
        run_manual_source_mode(output_dir)


if __name__ == "__main__":
    main()
