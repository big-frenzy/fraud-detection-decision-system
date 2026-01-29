
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Load model + columns (must be in same folder as app.py)
rf_model = joblib.load("rf_fraud_model.joblib")
feature_columns = joblib.load("feature_columns.joblib")

def show_decision(decision: str):
    if decision == "ALLOW":
        st.success("Decision: ALLOW ✅")
    elif decision == "REVIEW":
        st.warning("Decision: REVIEW 👀")
    else:
        st.error("Decision: BLOCK ⛔")


st.set_page_config(page_title="Fraud Detection", layout="centered")
st.title("Fraud Detection – Triage System")
st.info("Model: Random Forest | Policy: t_review=0.20 (send to human review), t_block=0.99 (auto-block).")
st.write("Random Forest fraud detection with ALLOW / REVIEW / BLOCK decisions.")

# Threshold sliders (your final policy defaults)
t_review = st.slider("Review threshold (t_review)", 0.0, 1.0, 0.2, 0.01)
t_block = st.slider("Block threshold (t_block)", 0.0, 1.0, 0.99, 0.01)

if t_review >= t_block:
    st.error("t_review must be less than t_block")
    st.stop()

st.divider()

# ✅ Evidence: show the performance you achieved
st.subheader("Offline Results (Test Set)")
st.write("- Fraud caught by REVIEW+BLOCK: **94 / 98**")
st.write("- Innocent auto-blocked: **17**")
st.write("- Outputs: **ALLOW / REVIEW / BLOCK**")

st.divider()

st.subheader("Model Insight (Global Feature Importance)")
st.caption("Top features the model relies on when detecting fraud.")
importances = pd.Series(rf_model.feature_importances_, index=feature_columns).sort_values(ascending=False)
st.dataframe(importances.head(10))

# We'll use these for simple local explanation
top_features = list(importances.head(5).index)

st.divider()

# Optional: demo mode (pick a row from X_test if available)
st.subheader("Demo Mode")
st.caption("Pick a transaction index from X_test.csv to test quickly.")

demo_available = False
examples_available = False

try:
    X_test = pd.read_csv("X_test.csv", index_col=0)
    y_test = pd.read_csv("y_test.csv", index_col=0).iloc[:, 0]
    demo_available = True
except Exception:
    demo_available = False

try:
    X_examples = pd.read_csv("examples.csv", index_col=0)
    examples_available = True
except Exception:
    examples_available = False

if demo_available:
    idx = st.number_input("Transaction index (row id)", value=int(X_test.index[0]), step=1)

    if idx in X_test.index:
        X_one = X_test.loc[[idx]][feature_columns]

        if st.button("Predict (Demo)"):
            prob = rf_model.predict_proba(X_one)[0, 1]
            decision = "BLOCK" if prob >= t_block else ("REVIEW" if prob >= t_review else "ALLOW")

            st.metric("Fraud probability", f"{prob:.3f}")
            show_decision(decision)
            st.write(f"True label (demo): {int(y_test.loc[idx])}  (1=Fraud, 0=Normal)")

            # ✅ Simple local explanation: show top-risk signals for this row
            st.subheader("Local Signals (Top Features)")
            st.caption("These are the most influential features globally, shown for this specific transaction.")
            st.dataframe(X_one[top_features].T.rename(columns={X_one.index[0]: "value"}))

    else:
        st.warning("That index is not in X_test.csv. Try another.")
else:
    st.info("Demo mode not available yet. (Create X_test.csv and y_test.csv to enable it.)")

st.divider()

# Fixed demo examples (must exist in X_test.csv)
ALLOW_EXAMPLE_IDX = 43800
REVIEW_EXAMPLE_IDX = 12890
BLOCK_EXAMPLE_IDX = 14920

# Manual input mode
st.subheader("Manual Input (All Features)")
st.caption("Enter feature values manually if you don't have demo CSVs.")

# Persist manual values across reruns
if "manual_values" not in st.session_state:
    st.session_state.manual_values = {col: 0.0 for col in feature_columns}

st.write("Quick load examples into Manual Input:")
c1, c2, c3 = st.columns(3)

def load_row_into_manual(idx: int):
    row = X_examples.loc[idx, feature_columns]
    st.session_state.manual_values = {col: float(row[col]) for col in feature_columns}

# Buttons
with c1:
    if st.button("Load ALLOW example"):
        if examples_available and (ALLOW_EXAMPLE_IDX in X_examples.index):
            load_row_into_manual(ALLOW_EXAMPLE_IDX)
        else:
            st.info("ALLOW example not available yet.")

with c2:
    if st.button("Load REVIEW example"):
        if examples_available and (REVIEW_EXAMPLE_IDX in X_examples.index):
            load_row_into_manual(REVIEW_EXAMPLE_IDX)
        else:
            st.info("REVIEW example not available yet.")

with c3:
    if st.button("Load BLOCK example"):
        if examples_available and (BLOCK_EXAMPLE_IDX in X_examples.index):
            load_row_into_manual(BLOCK_EXAMPLE_IDX)
        else:
            st.info("BLOCK example not available yet.")

input_data = {}
for col in feature_columns:
    input_data[col] = st.number_input(
        col,
        value=float(st.session_state.manual_values.get(col, 0.0))
    )

# keep state updated
st.session_state.manual_values = input_data

X_manual = pd.DataFrame([input_data], columns=feature_columns)

if st.button("Predict (Manual)"):
    prob = rf_model.predict_proba(X_manual)[0, 1]
    decision = "BLOCK" if prob >= t_block else ("REVIEW" if prob >= t_review else "ALLOW")

    st.metric("Fraud probability", f"{prob:.3f}")
    show_decision(decision)

    # ✅ Simple local explanation for manual input too
    st.subheader("Local Signals (Top Features)")
    st.caption("These are the most influential features globally, shown for your input.")
    st.dataframe(X_manual[top_features].T.rename(columns={0: "value"}))

st.divider()

# ✅ Responsible AI note
st.caption(
    "Note: This is a decision-support demo. 'BLOCK' is reserved for very high-confidence cases. "
    "Uncertain cases are routed to 'REVIEW' to reduce harm to legitimate users."
)
