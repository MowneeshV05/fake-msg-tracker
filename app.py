# app.py - Streamlit Web Interface for the Scam Message Checker
# Features: Dual-Engine (ML + Rules), Image/Screenshot OCR, and Regional Hinglish Support

import streamlit as st
import importlib
import model
import rules
import ocr_reader
from PIL import Image

# Ensure rules module is always freshly loaded
importlib.reload(rules)

# Set page title, icon, and centered layout
st.set_page_config(
    page_title="Fraud Message Tracking System",
    page_icon="🛡️",
    layout="centered"
)

# -------------------------------------------------------------
# STEP 1: Cache and load the machine learning model
# -------------------------------------------------------------
@st.cache_resource
def get_trained_classifier():
    # Trains the TF-IDF vectorizer and Logistic Regression model once on startup
    classifier, vectorizer = model.train_model("data/messages.csv")
    return classifier, vectorizer

# Load model and vectorizer
classifier, vectorizer = get_trained_classifier()

# -------------------------------------------------------------
# STEP 2: Risk calculation helper function
# -------------------------------------------------------------
def calculate_risk_level(scam_probability, flag_count, is_hindi=False):
    # High Risk condition: multiple red flags or high ML probability
    if scam_probability >= 70.0 or flag_count >= 3:
        if is_hindi:
            return "🚨 उच्च जोखिम (HIGH RISK - संभावित धोखाधड़ी)", "red", "चेतावनी: इस संदेश के किसी भी लिंक पर क्लिक न करें और न ही कोई विवरण साझा करें!"
        return "HIGH RISK", "red", "🚨 Scam Warning: Do NOT interact with this message or click any links!"
    
    # Medium Risk condition: some red flags or moderate ML probability
    elif scam_probability >= 40.0 or flag_count >= 1:
        if is_hindi:
            return "⚠️ मध्यम जोखिम (MEDIUM RISK - संदिग्ध संदेश)", "orange", "सावधानी: यह संदेश संदिग्ध लगता है। कोई भी कदम उठाने से पहले पुष्टि करें।"
        return "MEDIUM RISK", "orange", "⚠️ Caution: This message shows suspicious patterns. Verify before acting."
    
    # Low Risk condition
    else:
        if is_hindi:
            return "✅ कम जोखिम (LOW RISK - सुरक्षित)", "green", "सुरक्षित: इस संदेश में कोई स्पष्ट धोखाधड़ी या खतरे के संकेत नहीं मिले।"
        return "LOW RISK", "green", "✅ Safe: No obvious scam indicators detected."

# -------------------------------------------------------------
# STEP 3: Header Section
# -------------------------------------------------------------
st.title("🛡️ Fraud Message Tracking System")
st.write(
    "Detect and track suspicious SMS, WhatsApp messages, or **upload screenshots** to catch fraud "
    "(KYC blocks, electricity cuts, lottery fraud, UPI refund traps) with plain-English & Hindi explanations."
)

# -------------------------------------------------------------
# STEP 4: Sidebar Options (Language + Quick Demo Samples)
# -------------------------------------------------------------
st.sidebar.header("🌐 Language / भाषा")
lang_choice = st.sidebar.radio("Explanation Language:", ["English", "हिंदी / Hinglish"])
is_hindi_selected = (lang_choice == "हिंदी / Hinglish")
lang_code = "hi" if is_hindi_selected else "en"

st.sidebar.divider()
st.sidebar.header("💡 Try Sample Messages")
st.sidebar.write("Click any sample for instant testing:")

# Pre-defined sample messages including Hinglish for judges
sample_options = [
    "-- Select a sample message --",
    "SBI Bank KYC Block Threat (English Scam)",
    "Electricity Power Disconnection (Hinglish Scam)",
    "KBC Lucky Draw Lottery (English Scam)",
    "PhonePe UPI Cashback QR Scam (Hinglish Scam)",
    "Swiggy Delivery Login OTP (Safe)",
    "Official Bank Credit Alert (Safe)"
]

sample_choice = st.sidebar.selectbox("Choose a sample:", sample_options)

default_text = ""
if sample_choice == "SBI Bank KYC Block Threat (English Scam)":
    default_text = "Dear Customer, Your SBI Bank account has been blocked due to incomplete KYC. Update immediately at http://bit.ly/sbi-kyc-verify"
elif sample_choice == "Electricity Power Disconnection (Hinglish Scam)":
    default_text = "Priy grahak, aapka bijli connection aaj raat 9:30 baje kat diya jayega kyunki bill baki hai. Turant sampark kare 9876501234"
elif sample_choice == "KBC Lucky Draw Lottery (English Scam)":
    default_text = "Congratulations! You have won Rs 25,00,000 in Kaun Banega Crorepati WhatsApp lucky draw. Send claim fee Rs 500 to UPI id kbcwinner@okaxis"
elif sample_choice == "PhonePe UPI Cashback QR Scam (Hinglish Scam)":
    default_text = "Dear user aapko PhonePe par 3000 cashback mila hai. Paise lene ke liye QR code scan karke apna UPI PIN dale"
elif sample_choice == "Swiggy Delivery Login OTP (Safe)":
    default_text = "Your OTP for logging into Swiggy is 492018. Valid for 10 minutes. Do not share your OTP with anyone, even customer care executives."
elif sample_choice == "Official Bank Credit Alert (Safe)":
    default_text = "Your SBI account XX4321 is credited with INR 35,000 on 28-Sep. Available balance is INR 48,250. - State Bank of India"

# -------------------------------------------------------------
# STEP 5: Input Tabs (Text Input vs Image Upload)
# -------------------------------------------------------------
tab1, tab2 = st.tabs(["📝 Paste Message Text", "📸 Upload Screenshot / Picture"])

message_to_analyze = ""

with tab1:
    text_input = st.text_area(
        "Paste message text:",
        value=default_text,
        height=120,
        placeholder="Paste your SMS or WhatsApp message here..."
    )
    if text_input:
        message_to_analyze = text_input

with tab2:
    uploaded_image = st.file_uploader(
        "Upload a screenshot of the WhatsApp or SMS message (PNG, JPG):",
        type=["png", "jpg", "jpeg"]
    )
    
    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Screenshot", use_container_width=True)
        
        # Extract text using our native Windows OCR reader
        with st.spinner("🔍 Reading text from screenshot via OCR..."):
            extracted = ocr_reader.extract_text_from_image(uploaded_image)
            
        st.success("✅ Text Extracted from Screenshot:")
        extracted_text_box = st.text_area("Extracted text (you can edit if needed):", value=extracted, height=100)
        message_to_analyze = extracted_text_box

# Check button to trigger the analysis
check_button = st.button("🔍 Check for Scams", type="primary", use_container_width=True)

# -------------------------------------------------------------
# STEP 6: Run Analysis when Button is clicked
# -------------------------------------------------------------
if check_button:
    cleaned_input = message_to_analyze.strip()
    
    if len(cleaned_input) == 0:
        st.warning("Please paste a message or upload an image before clicking Check.")
    else:
        # Step A: Run Machine Learning Prediction
        ml_result = model.predict_message(cleaned_input, classifier, vectorizer)
        scam_prob = ml_result["scam_probability"]
        safe_prob = ml_result["safe_probability"]
        
        # Step B: Run Rule-Based Red Flag Detection (with selected language)
        rule_result = rules.analyze_rules(cleaned_input, language=lang_code)
        reasons_list = rule_result["reasons"]
        flag_count = rule_result["flag_count"]
        
        # Step C: Determine overall Risk Level
        risk_title, risk_color, risk_advice = calculate_risk_level(scam_prob, flag_count, is_hindi_selected)
        
        st.divider()
        
        # Step D: Display Risk Banner
        if risk_color == "red":
            st.error(f"### {risk_title}\n{risk_advice}")
        elif risk_color == "orange":
            st.warning(f"### {risk_title}\n{risk_advice}")
        else:
            st.success(f"### {risk_title}\n{risk_advice}")
            
        # Step E: Display Machine Learning Metrics
        st.subheader("📊 Machine Learning Assessment" if not is_hindi_selected else "📊 मशीन लर्निंग परिणाम")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Scam Probability" if not is_hindi_selected else "धोखाधड़ी की संभावना", f"{scam_prob}%")
        with col2:
            st.metric("Safe Probability" if not is_hindi_selected else "सुरक्षित होने की संभावना", f"{safe_prob}%")
            
        # Progress bar for visual probability
        st.progress(scam_prob / 100.0)
        
        # Step F: Display Explainable AI Reasons
        st.subheader("🧐 Why did the system make this decision?" if not is_hindi_selected else "🧐 यह निर्णय क्यों लिया गया?")
        if len(reasons_list) > 0:
            st.write("Red flags detected in the message:" if not is_hindi_selected else "संदेश में पाए गए खतरे के संकेत:")
            for reason in reasons_list:
                st.markdown(f"- 🔴 **{reason}**")
        else:
            if is_hindi_selected:
                st.markdown("- 🟢 **कोई जल्दबाजी, पिन/ओटीपी की मांग, या खतरनाक लिंक नहीं मिला।**")
            else:
                st.markdown("- 🟢 **No psychological pressure words, credential requests, or dangerous links found.**")
            
        # Step G: Educational Safety Guidance
        if is_hindi_selected:
            st.info(
                "💡 **नागरिक सुरक्षा सलाह:**\n"
                "- बैंक या सरकारी विभाग कभी भी फोन/एसएमएस पर OTP, UPI PIN या ATM PIN नहीं मांगते।\n"
                "- पैसे प्राप्त करने (Receive) के लिए कभी भी UPI PIN दर्ज करने की आवश्यकता नहीं होती।\n"
                "- साइबर फ्रॉड की शिकायत दर्ज करने के लिए **1930** पर कॉल करें या **cybercrime.gov.in** पर जाएं।"
            )
        else:
            st.info(
                "💡 **Citizen Safety Guidance:**\n"
                "- Banks and official agencies will **never** ask for OTP, UPI PIN, or ATM PIN.\n"
                "- You **never** need to enter your UPI PIN to receive money or cashbacks.\n"
                "- To report cyber fraud in India, dial the National Cyber Crime Helpline at **1930** or visit **cybercrime.gov.in**."
            )

# -------------------------------------------------------------
# Footer
# -------------------------------------------------------------
st.divider()
st.caption("Fraud Message Tracking System | AI & Data Science Hackathon Project | Features: Streamlit UI + Windows OCR + TF-IDF ML + Bilingual Heuristics")
