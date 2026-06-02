import streamlit as st

from visaflow.config import SAMPLES_DIR
from visaflow.ingestion.loaders import load_document
from visaflow.extraction.extractors import extract_information
from visaflow.planning.planner import build_task_plan
from visaflow.drafting.drafter import draft_response_with_mode, generate_next_step_summary


st.set_page_config(page_title="VisaFlow", layout="wide")

st.title("VisaFlow")
st.caption("AI operations agent for international-student bureaucracy")

sample_files = sorted([p.name for p in SAMPLES_DIR.glob("*.txt")])

with st.sidebar:
    st.header("Demo Controls")
    selected_file = st.selectbox("Choose a sample file", sample_files)
    enhanced_draft = st.checkbox("Use enhanced draft mode", value=True)
    run_pipeline = st.button("Run pipeline")

if run_pipeline:
    document = load_document(SAMPLES_DIR / selected_file)
    extracted = extract_information(document.text)
    plan = build_task_plan(extracted)
    draft = draft_response_with_mode(plan, enhanced=enhanced_draft)
    summary = generate_next_step_summary(plan)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Source", "Extracted Info", "Plan", "Summary", "Draft"]
    )

    with tab1:
        st.subheader("Source Document")
        st.text_area("Source text", document.text, height=350)

    with tab2:
        st.subheader("Extracted Information")
        st.write("**Deadlines**")
        st.write(extracted.get("deadlines", []))
        st.write("**Requested documents**")
        st.write(extracted.get("requested_documents", []))
        st.write("**Action items**")
        st.write(extracted.get("action_items", []))

        evidence = extracted.get("evidence", {})
        if evidence:
            st.write("**Evidence**")
            for category, items in evidence.items():
                if items:
                    st.write(f"**{category}**")
                    for item, snippet in items.items():
                        st.write(f"- {item}: {snippet}")

    with tab3:
        st.subheader("Planned Tasks")
        for task in plan.tasks:
            st.write(
                {
                    "task": task.task,
                    "priority": task.priority,
                    "workflow_type": task.workflow_type,
                    "depends_on": task.depends_on,
                }
            )

    with tab4:
        st.subheader("Next-Step Summary")
        st.text(summary)

    with tab5:
        st.subheader("Draft Response")
        st.text(draft)
else:
    st.info("Choose a sample file and click 'Run pipeline' to start.")
