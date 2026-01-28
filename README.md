# Fraud Detection Decision-Support System

An end-to-end fraud detection decision-support system that outputs **ALLOW / REVIEW / BLOCK** based on predicted fraud risk.

## What this is
Instead of only predicting fraud vs non-fraud, the system estimates a **fraud probability** and applies a triage policy:

- **ALLOW**: probability < t_review  
- **REVIEW**: t_review ≤ probability < t_block  
- **BLOCK**: probability ≥ t_block  

Default policy:
- t_review = 0.20
- t_block = 0.99

## Why it matters
Fraud detection is not just about accuracy. False positives can harm legitimate users, while false negatives can miss fraud. This project demonstrates risk-based decision making with a human-in-the-loop review stage.

## Explainability
- **Global**: Random Forest feature importance (top drivers of fraud risk)
- **Local**: shows key feature values for the chosen transaction/input

## Run locally

```bash
python3 -m streamlit run app.py

