import os
from datetime import datetime

import pandas as pd
import streamlit as st

from logic import analyze_hoa_ticket, ask_documents

st.set_page_config(
    page_title="Community Democracy AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

CSV_PATH = "requests.csv"

COLUMNS = [
    "id",
    "submitted_at",
    "submitted_by_role",
    "apartment_unit",
    "message_text",
    "category",
    "sentiment",
    "urgency",
    "status",
    "satisfaction_score"
]


def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = None
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)


def save_data(df):
    df.to_csv(CSV_PATH, index=False)


if "requests_df" not in st.session_state:
    st.session_state.requests_df = load_data()

# ---------- Styling ----------
st.markdown("""
<style>
.block-container {
    padding-top: 1.3rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}
h1, h2, h3 {
    letter-spacing: -0.02em;
}
.big-button button {
    width: 100%;
    height: 72px;
    font-size: 1.15rem;
    font-weight: 700;
    border-radius: 14px;
}
.action-card {
    padding: 1rem 1rem 0.8rem 1rem;
    border-radius: 16px;
    border: 1px solid rgba(200,200,200,0.22);
    margin-bottom: 0.9rem;
    background: rgba(250,250,250,0.02);
}
.section-box {
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid rgba(200,200,200,0.18);
    margin-bottom: 1rem;
    background: rgba(250,250,250,0.015);
}
.small-note {
    font-size: 0.9rem;
    opacity: 0.75;
}
</style>
""", unsafe_allow_html=True)

st.title("🏢 BOTANIC CENTER TOWN")
st.write(
    "A prototype for transparent apartment community governance — helping residents raise issues, vote on priorities,"
    "understand records, and helping managers coordinate communication and reporting."
)

main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
    "New Request",
    "Ask me anything!",
    "Resident Dashboard",
    "Manager Dashboard"
])

# =========================================================
# 1. NEW REQUEST INTAKE
# =========================================================
with main_tab1:
    st.header("New Request")
    st.write(
        "Use this form to intake a resident message, classify it, and add it to the shared request log."
    )

    with st.form("request_form"):
        submitted_by_role = st.selectbox("Submitted by", ["resident", "manager"])
        apartment_unit = st.text_input("Apartment unit (optional)")
        message_text = st.text_area(
            "Resident message or issue description",
            placeholder="The hallway lights on the 3rd floor are out again."
        )

        st.markdown("**Example questions**")
        st.write("- There is water leakage in the garage. Send someone quickly!")
        st.write("- Can we build a shed for elders near 5th block")

        submit_request = st.form_submit_button("Analyze and Save Request")

    if submit_request:
        if message_text.strip():
            with st.spinner("Analyzing request..."):
                result = analyze_hoa_ticket(message_text)

            current_df = st.session_state.requests_df
            next_id = 1 if current_df.empty else int(current_df["id"].max()) + 1

            new_row = {
                "id": next_id,
                "submitted_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "submitted_by_role": submitted_by_role,
                "apartment_unit": apartment_unit,
                "message_text": message_text,
                "category": result["category"],
                "sentiment": result["sentiment"],
                "urgency": result["urgency"],
                "status": "Open",
                "satisfaction_score": None
            }

            st.session_state.requests_df = pd.concat(
                [st.session_state.requests_df, pd.DataFrame([new_row])],
                ignore_index=True
            )
            save_data(st.session_state.requests_df)

            st.success(f"Your ticket has been created. Your ticket number is {next_id}. We will get back to you soon.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Category", result["category"])
            col2.metric("Sentiment", result["sentiment"])
            col3.metric("Urgency", result["urgency"])

            st.info(f"**English Summary / Translation:** {result['english_translation']}")
        else:
            st.warning("Please enter a request before submitting.")

# =========================================================
# 2. ASK ABOUT COMMUNITY DOCUMENTS
# =========================================================
with main_tab2:
    st.header("Ask me anything!")
    st.write(
        "Ask questions about budgets, rules, meeting decisions, and other official community records."
    )

    doc_question = st.text_input(
        "Your question",
        placeholder="How was money spent this quarter?"
    )

    st.markdown("**Example questions**")
    st.write("- How was money spent this quarter?")
    st.write("- What are the quiet hours?")
    st.write("- What was decided about elevator safety?")
    st.write("- What issues are residents raising most often?")

    if st.button("Search Community Documents", key="doc_search"):
        if doc_question.strip():
            with st.spinner("Searching community documents..."):
                answer = ask_documents(doc_question)
            st.success("Answer generated")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

# =========================================================
# 3. RESIDENT DASHBOARD
# =========================================================
with main_tab3:
    # Top metrics and headers have been removed for a cleaner public view

    resident_section1, resident_section2, resident_section3 = st.tabs([
        "Finance",
        "Future Actions",
        "What's Happening"
    ])

    with resident_section1:
        st.subheader("Monthly Spending Summary")

        # Sample finance table customized for the demo
        finance_data = {
            "Expense Category": ["Cleaning & Janitorial", "Staff Salaries", "Elevator Maintenance",
                                 "Roof & Plumbing Repairs", "Reserve Fund"],
            "Allocated Budget (MNT)": ["15,000,000", "30,000,000", "8,000,000", "20,000,000", "10,000,000"],
            "Spent YTD (MNT)": ["3,500,000", "7,500,000", "2,000,000", "15,500,000", "0"],
            "Status": ["🟢 On Track", "🟢 On Track", "🟢 On Track", "🔴 Over Budget", "🟢 Untouched"]
        }

        # Display the table cleanly without the index numbers on the left
        st.dataframe(pd.DataFrame(finance_data), use_container_width=True, hide_index=True)

        st.info(
            "ℹ️ LIVE finance module placeholder. In the production version, this table will sync directly with the HOA accounting software.")

    with resident_section2:
        st.subheader("Future Actions")
        st.write("Residents can signal support for future community improvements and follow-up priorities.")

        future_actions = [
            "Publish a clearer monthly spending summary",
            "Improve response tracking for repeated maintenance issues",
            "Create a clearer update process for elevator and roof repairs",
            "Share more transparent meeting follow-up notes",
            "Improve resident communication about timelines and responsibilities"
        ]

        for i, action in enumerate(future_actions, start=1):
            st.markdown(f'<div class="action-card"><strong>{i}. {action}</strong></div>', unsafe_allow_html=True)
            st.markdown('<div class="big-button">', unsafe_allow_html=True)
            if st.button(f"👍 Upvote This Future Action", key=f"upvote_action_{i}"):
                st.info("Upvote recorded in demo mode.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.caption("Demo placeholder: upvotes do not yet change rankings or priorities.")

    with resident_section3:
        st.subheader("What's Happening")
        st.write("This section gives residents a broad view of visible community activity and current requests.")

        rdf = st.session_state.requests_df.copy()

        if not rdf.empty:
            st.markdown("### Major Repeated Issues")
            issue_counts = (
                rdf.groupby("category")
                .size()
                .reset_index(name="count")
                .sort_values("count", ascending=False)
            )
            st.dataframe(issue_counts, use_container_width=True, hide_index=True)

            st.markdown("### Full Public Request Log")
            resident_view_df = rdf[[
                "id", "submitted_at", "category", "sentiment", "urgency", "status", "message_text"
            ]].sort_values("id", ascending=False)
            st.dataframe(resident_view_df, use_container_width=True, hide_index=True)
        else:
            st.info("No public request activity has been recorded yet.")

# =========================================================
# 4. MANAGER DASHBOARD
# =========================================================
with main_tab4:
    st.header("Manager Dashboard")
    st.write(
        "This internal view helps management review requests, understand patterns, prepare communication, and monitor public community signals."
    )

    manager_tab1, manager_tab2, manager_tab3 = st.tabs([
        "Operations View",
        "Manager Response Tools",
        "Social Media Watch"
    ])

    with manager_tab1:
        st.subheader("Operations View")

        mdf = st.session_state.requests_df.copy()

        if mdf.empty:
            st.info("No requests recorded yet.")
        else:
            mdf["satisfaction_score"] = pd.to_numeric(mdf["satisfaction_score"], errors="coerce")

            total_requests = len(mdf)
            open_requests = (mdf["status"] == "Open").sum()
            in_progress_requests = (mdf["status"] == "In Progress").sum()
            resolved_requests = (mdf["status"] == "Resolved").sum()

            sat_df = mdf[mdf["satisfaction_score"].notna()]
            satisfaction_rate = round((sat_df["satisfaction_score"].mean() / 5) * 100, 1) if not sat_df.empty else None

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("All Requests", total_requests)
            c2.metric("Open", int(open_requests))
            c3.metric("In Progress", int(in_progress_requests))
            c4.metric("Resolved", int(resolved_requests))

            st.markdown("### Community Trends")

            left2, right2 = st.columns(2)

            with left2:
                st.write("**Repeated issues by category**")
                issue_counts = (
                    mdf.groupby("category")
                    .size()
                    .reset_index(name="count")
                    .sort_values("count", ascending=False)
                )
                st.dataframe(issue_counts, use_container_width=True, hide_index=True)

            with right2:
                st.write("**Sentiment breakdown**")
                sentiment_counts = (
                    mdf.groupby("sentiment")
                    .size()
                    .reset_index(name="count")
                    .sort_values("count", ascending=False)
                )
                st.dataframe(sentiment_counts, use_container_width=True, hide_index=True)

            st.markdown("### Full Internal Request Log")
            st.dataframe(mdf.sort_values("id", ascending=False), use_container_width=True, hide_index=True)

            st.markdown("### Community Satisfaction")
            if satisfaction_rate is not None:
                st.metric("Satisfaction Rate", f"{satisfaction_rate}%")
            else:
                st.info("No satisfaction ratings recorded yet.")

    with manager_tab2:
        st.subheader("Manager Response Tools")
        st.write(
            "Select a request, review its details, update status, and prepare a future resident response."
        )

        mdf = st.session_state.requests_df.copy()

        if mdf.empty:
            st.info("No requests available yet.")
        else:
            request_ids = mdf["id"].tolist()
            selected_id = st.selectbox("Select Request ID", request_ids)

            row = mdf[mdf["id"] == selected_id].iloc[0]

            st.markdown("### Selected Request")
            st.write(f"**Submitted at:** {row['submitted_at']}")
            st.write(f"**Submitted by:** {row['submitted_by_role']}")
            st.write(f"**Apartment unit:** {row['apartment_unit']}")
            st.write(f"**Category:** {row['category']}")
            st.write(f"**Sentiment:** {row['sentiment']}")
            st.write(f"**Urgency:** {row['urgency']}")
            st.write(f"**Current status:** {row['status']}")
            st.write(f"**Message:** {row['message_text']}")

            st.markdown('<div class="big-button">', unsafe_allow_html=True)
            if st.button("✉️ Generate Response", key="manager_generate_response"):
                st.info("Response generation placeholder. This button currently does not perform any action.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.caption("Demo placeholder: in a future version this would draft a resident-facing response.")

            new_status = st.selectbox("Update request status", ["Open", "In Progress", "Resolved"])
            new_satisfaction = st.selectbox("Record satisfaction score", ["", 1, 2, 3, 4, 5])

            if st.button("Save Request Updates", key="manager_save_updates"):
                idx = st.session_state.requests_df.index[st.session_state.requests_df["id"] == selected_id][0]
                st.session_state.requests_df.at[idx, "status"] = new_status

                if new_satisfaction != "":
                    st.session_state.requests_df.at[idx, "satisfaction_score"] = int(new_satisfaction)

                save_data(st.session_state.requests_df)
                st.success("Request updated successfully.")

    with manager_tab3:
        st.subheader("Social Media Watch")
        st.write(
            "Placeholder for future monitoring of public resident discussions, repeated social concerns, and emerging community issues."
        )

        st.info("Social Media Watch placeholder. In a future version, this area could summarize recurring topics, sentiment shifts, and frequently raised issues from community social channels.")

        st.markdown("### Example Future Monitoring Features")
        st.write("- Repeated issue detection from public community posts")
        st.write("- Community sentiment tracking over time")
        st.write("- Escalation alerts for urgent or repeated complaints")
        st.write("- Early signals for finance or maintenance concerns")