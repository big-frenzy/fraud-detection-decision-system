# Fraud Detection Decision-Support System

## Live Demo
🔗 https://fraud-detection-decision-system.streamlit.app

An end-to-end fraud detection decision-support system that outputs **ALLOW / REVIEW / BLOCK** based on predicted fraud risk.

## Screenshots

### Overview (Policy + thresholds)
![Overview](screenshots/01_overview.png)

### Global Feature Importance
![Feature Importance](screenshots/02_feature_importance.png)

### Example: BLOCK (high confidence fraud)
![BLOCK Example](screenshots/03_block.png)

### Example: REVIEW (send to human review)
![REVIEW Example](screenshots/04_review.png)

### Example: ALLOW (low risk transaction)
![ALLOW Example](screenshots/05_allow.png)

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

