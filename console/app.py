import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GuardianAI Forensic Console", layout="wide")
st.title("GuardianAI v2 — Compliance Forensic Console")
st.caption("Portfolio demo — OFAC/FinCEN-style framing, not connected to live regulatory systems")

cases = pd.read_csv('data/processed/scored_cases.csv')
qa_log = pd.read_csv('data/processed/qa_audit_log.csv')

st.subheader("Flagged Cases Queue")
flagged = cases[cases['flagged']==1].sort_values('risk_score', ascending=False)
st.write(f"{len(flagged)} cases flagged for review")

selected_txn = st.selectbox("Select a case to review", flagged['txn_id'].tolist())
case = cases[cases['txn_id']==selected_txn].iloc[0]

col1, col2 = st.columns(2)
with col1:
    st.metric("Risk Score", f"{case['risk_score']:.4f}")
    st.write("**From account:**", case['from_account'])
    st.write("**To account:**", case['to_account'])
    st.write("**Amount:**", f"${case['amount_paid']:,.2f}")
    st.write("**Payment format:**", case['payment_format'])
with col2:
    st.write("**Top risk drivers (SHAP):**")
    st.write(case['top_drivers'])

st.subheader("Case Review")
decision = st.radio("Decision", ["Escalate", "Clear — false positive", "Needs more info"])
reviewer = st.text_input("Reviewer name", "analyst_1")
notes = st.text_area("Notes")

if st.button("Submit review"):
    new_row = pd.DataFrame([{
        'txn_id': selected_txn, 'reviewer': reviewer, 'decision': decision,
        'notes': notes, 'timestamp': datetime.now().isoformat()
    }])
    qa_log = pd.concat([qa_log, new_row], ignore_index=True)
    qa_log.to_csv('data/processed/qa_audit_log.csv', index=False)
    st.success("Review logged.")

st.subheader("QA Audit Trail")
st.dataframe(qa_log.tail(20))
