# 🛡️ Fraud Message Tracking System

An AI-based web app that checks SMS and WhatsApp messages for scams and tells you how risky they are, with the reasons explained in **English and Hindi**.

## 🔗 Live Demo
**👉 [https://fake-msg-tracker-identifythecriminal.streamlit.app/](https://fake-msg-tracker-identifythecriminal.streamlit.app/)**

> Free apps sleep when unused. If you see a "Wake up" button, click it and wait a few seconds.

## ✨ Features
- **ML detection:** TF-IDF + Logistic Regression (scikit-learn) gives scam and safe probabilities.
- **Rule-based engine** for English and Hinglish that flags urgency threats, OTP/PIN requests, prize bait, authority impersonation and unsafe links.
- **Risk level:** combines the ML score and rule score into Low / Medium / High.
- **Explanations** in English and Hindi.
- **Screenshot upload:** reads the message text from an image using OCR.
- **Safety guidance** with the national cyber crime helpline **1930**.

## 🧰 Tech Stack
Python · Streamlit · scikit-learn · pandas · Pillow · Tesseract OCR (pytesseract)

## 📁 Project Structure
| File | Purpose |
|------|---------|
| `app.py` | Streamlit user interface |
| `ocr_reader.py` | Extracts text from screenshots (Tesseract on cloud, Windows OCR as fallback) |
| `requirements.txt` | Python dependencies |
| `packages.txt` | System packages for deployment (`tesseract-ocr`) |

## ▶️ Run Locally
```bash
git clone https://github.com/MowneeshV05/fake-msg-tracker.git
cd fake-msg-tracker
pip install -r requirements.txt
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

## ☁️ Deployment
Deployed on **Streamlit Community Cloud**. Every push to the `main` branch redeploys the app automatically.

## 🚨 Reporting Fraud
If you receive or fall for a scam, call **1930** or report at [cybercrime.gov.in](https://cybercrime.gov.in).

## 👤 Author
**Mowneesh Veerakumar** — B.Tech AI & Data Science, Sri Eshwar College of Engineering
[GitHub](https://github.com/MowneeshV05) · [LinkedIn](https://www.linkedin.com/in/mowneesh-v-b4b59a432/)
