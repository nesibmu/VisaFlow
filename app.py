import streamlit as st

from visaflow.config import SAMPLES_DIR
from visaflow.ingestion.loaders import load_document
from visaflow.extraction.extractors import extract_information
from visaflow.planning.planner import build_task_plan
import visaflow.drafting.drafter as drafter


DEFAULT_PRESET = "Mixed admin case"

DEMO_PRESETS = {
    "Mixed admin case": {
        "text": """Subject: Follow-up on housing and immigration documents

Hello Nesib,

To complete your file, please upload your signed housing agreement, a recent bank statement, a copy of your passport, and your current I-20 by June 15, 2026 through the student portal.

Please confirm once the documents have been uploaded. If you expect any delay, reply to this message as soon as possible.

Best,
Student Services""",
        "note": "Best default demo. Shows multiple requested documents, a deadline, and follow-up actions.",
    },
    "Escalated admin case": {
        "text": """Subject: Urgent follow-up on housing, financial aid, and immigration items

Hello Nesib,

We are still missing your signed housing agreement, updated bank statement, current passport copy, current I-20, and statement of support.

Please upload all materials through the student portal by June 10, 2026. You should also reply to this email by June 8, 2026 if you expect any delay. Once everything has been uploaded, please confirm completion so we can finish the review.

Best,
Student Services and Financial Support""",
        "note": "Best dense case. Shows multiple deadlines and stronger urgency.",
    },
    "Housing follow-up": {
        "text": """Subject: Additional documents needed for spring housing approval

Hello Nesib,

To complete your housing review, please submit your updated housing contract request and a recent bank statement by May 28, 2026. You should also upload a copy of your passport and current I-20 through the student portal.

Please confirm once the materials have been uploaded. If you need an extension, respond to this message as soon as possible.

Best,
Housing Assignments""",
        "note": "Simple case for a clean walkthrough.",
    },
    "Financial aid review": {
        "text": """Subject: Missing documents for financial aid review

Hello Nesib,

We reviewed your file and still need a signed statement of support and your most recent bank statement.

Please upload both documents by June 3, 2026. If you are unable to meet this deadline, reply to this email as soon as possible.

Best,
Financial Aid Office""",
        "note": "Good for showing sentence-based extraction.",
    },
    "Immigration update": {
        "text": """Subject: Missing immigration documents

Hello,

To complete your record, please upload a copy of your passport and your current I-20 by June 12, 2026 through the student portal.

Please confirm once the materials have been uploaded.

Best,
International Student Office""",
        "note": "Good for showing immigration-specific workflow tagging.",
    },
    "Weak noisy case": {
        "text": """Subject: quick follow up

hi, just checking in on the file. send what you can soon and let us know if anything changed.

thanks""",
        "note": "Best robustness case. Shows fallback behavior on incomplete input.",
    },
}


def safe_call(name, *args, fallback=""):
    fn = getattr(drafter, name, None)
    if fn is None:
        return fallback
    try:
        return fn(*args)
    except Exception:
        return fallback


def run_pipeline_from_text(text: str):
    extracted = extract_information(text)
    plan = build_task_plan(extracted)

    summary = safe_call(
        "generate_next_step_summary",
        plan,
        fallback="No summary available.",
    )
    short_summary = safe_call(
        "generate_short_summary",
        plan,
        extracted,
        fallback="Short summary unavailable.",
    )
    recommended_next_action = safe_call(
        "generate_recommended_next_action",
        plan,
        fallback="No recommended next action available.",
    )
    checklist = safe_call(
        "generate_action_checklist",
        plan,
        fallback="Checklist unavailable.",
    )
    ops_handoff = safe_call(
        "generate_ops_handoff",
        plan,
        extracted,
        fallback="Operations handoff unavailable.",
    )
    email_ready_reply = safe_call(
        "generate_email_ready_reply",
        plan,
        fallback="Email-ready reply unavailable.",
    )
    task_digest = safe_call(
        "generate_task_digest",
        plan,
        extracted,
        fallback="Task digest unavailable.",
    )
    baseline_draft = safe_call(
        "draft_response_with_mode",
        plan,
        False,
        fallback="Baseline draft unavailable.",
    )
    enhanced_draft = safe_call(
        "draft_response_with_mode",
        plan,
        True,
        fallback="Enhanced draft unavailable.",
    )

    return {
        "source_text": text,
        "extracted": extracted,
        "plan": plan,
        "summary": summary,
        "short_summary": short_summary,
        "recommended_next_action": recommended_next_action,
        "checklist": checklist,
        "ops_handoff": ops_handoff,
        "email_ready_reply": email_ready_reply,
        "task_digest": task_digest,
        "baseline_draft": baseline_draft,
        "enhanced_draft": enhanced_draft,
    }


def compute_case_confidence(extracted: dict, plan) -> tuple:
    confidence_map = extracted.get("confidence", {})
    scores = []

    for category in ["deadlines", "requested_documents", "action_items"]:
        scores.extend(confidence_map.get(category, {}).values())

    signal_count = (
        len(extracted.get("deadlines", []))
        + len(extracted.get("requested_documents", []))
        + len(extracted.get("action_items", []))
    )

    if not scores or len(plan.tasks) == 0:
        return "low", 0.35

    avg = sum(scores) / len(scores)

    if signal_count >= 5 and avg >= 0.82:
        return "high", avg
    if signal_count >= 2 and avg >= 0.70:
        return "medium", avg
    return "low", avg


def badge_html(label: str) -> str:
    styles = {
        "high": ("#dcfce7", "#166534"),
        "medium": ("#fef3c7", "#92400e"),
        "low": ("#fee2e2", "#991b1b"),
    }
    bg, fg = styles.get(label, ("#f3f4f6", "#111827"))
    return f"<span style='background:{bg};color:{fg};padding:6px 10px;border-radius:999px;font-size:14px;font-weight:700;'>{label}</span>"


def render_task_card(task):
    color = {
        "high": "#ef4444",
        "medium": "#f59e0b",
        "low": "#9ca3af",
    }.get(getattr(task, "priority", "low"), "#9ca3af")

    status = getattr(task, "status", "ready")
    workflow = getattr(task, "workflow_type", "general")
    source = getattr(task, "source", "")
    urgency = getattr(task, "urgency_score", 0)
    depends_on = getattr(task, "depends_on", [])
    blocking_reason = getattr(task, "blocking_reason", "")

    depends_html = ""
    if depends_on:
        depends_html = f"<div style='margin-top:10px;font-size:15px;color:#6b7280;'><strong>Depends on:</strong> {', '.join(depends_on)}</div>"

    blocking_html = ""
    if blocking_reason:
        blocking_html = f"<div style='margin-top:10px;font-size:15px;color:#92400e;'><strong>Blocked because:</strong> {blocking_reason}</div>"

    st.markdown(
        f"""
<div style="border-left:8px solid {color};border-radius:16px;padding:18px 18px;margin-bottom:14px;background:#ffffff;border:1px solid #e5e7eb;">
  <div style="font-weight:800;font-size:20px;line-height:1.4;">{task.task}</div>
  <div style="margin-top:10px;font-size:15px;color:#4b5563;">
    <strong>Status:</strong> {status} &nbsp;&nbsp;•&nbsp;&nbsp;
    <strong>Workflow:</strong> {workflow} &nbsp;&nbsp;•&nbsp;&nbsp;
    <strong>Source:</strong> {source} &nbsp;&nbsp;•&nbsp;&nbsp;
    <strong>Priority:</strong> {getattr(task, "priority", "")} &nbsp;&nbsp;•&nbsp;&nbsp;
    <strong>Urgency:</strong> {urgency}
  </div>
  {depends_html}
  {blocking_html}
</div>
""",
        unsafe_allow_html=True,
    )


def render_list_section(title: str, items, confidence_map=None):
    st.markdown(f"### {title}")
    if not items:
        st.caption("None found.")
        return

    for item in items:
        score_html = ""
        if confidence_map is not None:
            score = confidence_map.get(item, 0.0)
            if score >= 0.9:
                label = "high"
            elif score >= 0.75:
                label = "medium"
            else:
                label = "low"
            score_html = badge_html(label)

        st.markdown(
            f"""
<div style="border:1px solid #e5e7eb;border-radius:14px;padding:14px 16px;margin-bottom:10px;background:white;display:flex;justify-content:space-between;align-items:center;gap:16px;">
  <div style="font-weight:700;font-size:18px;line-height:1.4;">{item}</div>
  <div>{score_html}</div>
</div>
""",
            unsafe_allow_html=True,
        )


st.set_page_config(page_title="VisaFlow", layout="wide")

st.markdown(
    """
<style>
.block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 16px;
    border-radius: 16px;
}
div[data-testid="stMetric"] label {
    font-size: 16px !important;
}
div[data-testid="stMetricValue"] {
    font-size: 28px !important;
}
textarea, input, select {
    font-size: 18px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

if "results" not in st.session_state:
    st.session_state.results = None

sample_files = sorted([p.name for p in SAMPLES_DIR.glob("*.txt")])

st.title("VisaFlow")
st.markdown(
    """
### AI operations agent for international-student bureaucracy

Use this app in **3 simple steps**:

**Step 1:** Choose how you want to provide input  
**Step 2:** Click **Run Workflow**  
**Step 3:** Review the extracted requirements, task plan, and ready-to-use outputs below
"""
)

st.divider()

st.markdown("## Step 1 — Choose your input")

input_mode = st.radio(
    "How do you want to provide input?",
    ["Demo preset", "Paste text", "Upload file", "Sample file"],
    horizontal=True,
)

selected_preset = DEFAULT_PRESET
pasted_text = ""
uploaded_file = None
selected_file = None

if input_mode == "Demo preset":
    selected_preset = st.selectbox("Choose a preset case", list(DEMO_PRESETS.keys()), index=0)
    st.info(DEMO_PRESETS[selected_preset]["note"])

elif input_mode == "Paste text":
    pasted_text = st.text_area(
        "Paste the full email or message here",
        height=260,
        placeholder="Paste the administrative email, request, or message here...",
    )

elif input_mode == "Upload file":
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

elif input_mode == "Sample file":
    selected_file = st.selectbox("Choose a sample file", sample_files)

st.markdown("## Step 2 — Run the workflow")
c1, c2 = st.columns([1, 1])
with c1:
    run_pipeline = st.button("Run Workflow", use_container_width=True)
with c2:
    clear_results = st.button("Clear Results", use_container_width=True)

if clear_results:
    st.session_state.results = None

if run_pipeline:
    source_text = ""

    if input_mode == "Demo preset":
        source_text = DEMO_PRESETS[selected_preset]["text"]
    elif input_mode == "Paste text":
        source_text = pasted_text.strip()
    elif input_mode == "Upload file":
        if uploaded_file is not None:
            source_text = uploaded_file.read().decode("utf-8").strip()
    elif input_mode == "Sample file":
        if selected_file:
            document = load_document(SAMPLES_DIR / selected_file)
            source_text = document.text

    if not source_text:
        st.warning("Please provide some input before running the workflow.")
    else:
        st.session_state.results = run_pipeline_from_text(source_text)

results = st.session_state.results

st.divider()
st.markdown("## Step 3 — Review the results")

if results is None:
    st.info("No results yet. Choose an input above and click Run Workflow.")
else:
    extracted = results["extracted"]
    plan = results["plan"]

    deadlines = extracted.get("deadlines", [])
    documents = extracted.get("requested_documents", [])
    actions = extracted.get("action_items", [])
    confidence = extracted.get("confidence", {})

    case_confidence_label, case_confidence_score = compute_case_confidence(extracted, plan)

    st.markdown(
        f"""
<div style="border:1px solid #dbeafe;border-radius:16px;padding:18px 20px;background:#eff6ff;margin-bottom:16px;">
  <div style="font-size:15px;color:#1d4ed8;margin-bottom:8px;font-weight:700;">Next Best Action</div>
  <div style="font-size:24px;font-weight:800;color:#1e3a8a;line-height:1.4;">{results["recommended_next_action"]}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div style="border:1px solid #e5e7eb;border-radius:16px;padding:18px 20px;background:#ffffff;margin-bottom:16px;">
  <div style="font-size:15px;color:#6b7280;margin-bottom:8px;font-weight:700;">Overall System Confidence</div>
  <div style="font-size:24px;font-weight:800;color:#111827;line-height:1.4;">{case_confidence_label} ({case_confidence_score:.2f})</div>
</div>
""",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Deadlines", len(deadlines))
    m2.metric("Documents", len(documents))
    m3.metric("Actions", len(actions))
    m4.metric("Tasks", len(plan.tasks))

    st.divider()

    st.markdown("### Original Input")
    st.text_area("Source text", results["source_text"], height=240)

    st.divider()

    c1, c2, c3 = st.columns(3)
    with c1:
        render_list_section("Deadlines", deadlines, confidence.get("deadlines", {}))
    with c2:
        render_list_section("Requested Documents", documents, confidence.get("requested_documents", {}))
    with c3:
        render_list_section("Action Items", actions, confidence.get("action_items", {}))

    st.divider()

    st.markdown("### Task Plan")
    if not plan.tasks:
        st.info("No task plan was generated from this input.")
    else:
        for task in plan.tasks:
            render_task_card(task)

    st.divider()

    st.markdown("### Outputs")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Short Summary",
            "Email Reply",
            "Task Digest",
            "Full Summary",
            "Enhanced Draft",
            "Checklist",
            "Operations Handoff",
        ]
    )

    with tab1:
        value = st.text_area("Short Summary", results["short_summary"], height=300)
        st.download_button("Export Short Summary", value, "visaflow_short_summary_export.txt", "text/plain")

    with tab2:
        value = st.text_area("Email Reply", results["email_ready_reply"], height=340)
        st.download_button("Export Email Reply", value, "visaflow_email_ready_reply_export.txt", "text/plain")

    with tab3:
        value = st.text_area("Task Digest", results["task_digest"], height=340)
        st.download_button("Export Task Digest", value, "visaflow_task_digest_export.txt", "text/plain")

    with tab4:
        value = st.text_area("Full Summary", results["summary"], height=340)
        st.download_button("Export Full Summary", value, "visaflow_summary_export.txt", "text/plain")

    with tab5:
        value = st.text_area("Enhanced Draft", results["enhanced_draft"], height=380)
        st.download_button("Export Enhanced Draft", value, "visaflow_enhanced_draft_export.txt", "text/plain")

    with tab6:
        value = st.text_area("Checklist", results["checklist"], height=380)
        st.download_button("Export Checklist", value, "visaflow_checklist_export.txt", "text/plain")

    with tab7:
        value = st.text_area("Operations Handoff", results["ops_handoff"], height=380)
        st.download_button("Export Operations Handoff", value, "visaflow_operations_handoff_export.txt", "text/plain")
