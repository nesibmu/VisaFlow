import sys
from visaflow.drafting.drafter import draft_reply, draft_summary
from visaflow.extraction.extractors import run_extraction
from visaflow.ingestion.loaders import load_document
from visaflow.planning.planner import build_plan
from visaflow.utils.render import render_extraction, render_plan



def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m visaflow.main <path-to-text-file>")
        return 1

    path = sys.argv[1]
    text = load_document(path)
    extraction = run_extraction(text)
    plan = build_plan(extraction)

    print(render_extraction(extraction))
    print(render_plan(plan))
    print("\nDRAFT EMAIL\n")
    print(draft_reply(plan))
    print("\nSUMMARY\n")
    print(draft_summary(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
