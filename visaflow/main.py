from visaflow.ingestion.loaders import load_text_file
from visaflow.extraction.extractors import extract_information
from visaflow.planning.planner import build_task_plan
from visaflow.drafting.drafter import draft_response
from visaflow.utils.render import render_result
from visaflow.config import SAMPLES_DIR


def run_demo(filename: str) -> str:
    path = SAMPLES_DIR / filename
    content = load_text_file(path)
    extracted = extract_information(content)
    plan = build_task_plan(extracted)
    response = draft_response(plan)
    return render_result(content, extracted, plan, response)


if __name__ == "__main__":
    print(run_demo("housing_email.txt"))
