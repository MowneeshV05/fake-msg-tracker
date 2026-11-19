# rules.py - Rule-based red flag detection engine for scam messages (English & Hinglish)

from url_checker import analyze_urls_in_message

# List 1: Urgency keywords in English and Indian Hinglish/Hindi
URGENCY_KEYWORDS = [
    # English
    "immediately",
    "urgent",
    "urgently",
    "24 hours",
    "blocked",
    "deactivated",
    "suspended",
    "disconnected",
    "freeze",
    "expires today",
    "expiring today",
    "tonight",
    "arrest",
    # Hinglish / Hindi
    "turant",
    "aaj raat",
    "24 ghante",
    "band ho jayega",
    "kat diya jayega",
    "kaat di jayegi",
    "rok diya gaya",
    "jaldi kare",
    "aakhri din"
]

# List 2: Sensitive security credentials in English and Hinglish
CREDENTIAL_KEYWORDS = [
    # English
    "otp",
    "cvv",
    "atm pin",
    "upi pin",
    "netbanking password",
    "enter pin",
    "share otp",
    "scan qr code",
    "scan this qr",
    # Hinglish / Hindi
    "otp bheje",
    "otp share kare",
    "pin dale",
    "upi pin dale",
    "password bataye",
    "qr scan kare"
]

# List 3: Unrealistic financial rewards, prizes, and job bait in English and Hinglish
REWARD_KEYWORDS = [
    # English
    "congratulations",
    "won rs",
    "lucky draw",
    "cashback refund",
    "instant cash",
    "bonus",
    "reward points",
    "earn daily",
    "0% interest",
    "processing fee",
    "claim fee",
    "free iphone",
    # Hinglish / Hindi
    "badhai ho",
    "lottery jeeti",
    "lottery jeeta",
    "inam mila",
    "shulk jama kare",
    "paise jeete",
    "roj kamaye"
]

# List 4: Impersonation of authority or public services in English and Hinglish
AUTHORITY_KEYWORDS = [
    # English
    "police",
    "cyber cell",
    "electricity power",
    "electricity officer",
    "income tax department",
    "court notice",
    "aadhaar update",
    "kyc update",
    # Hinglish / Hindi
    "bijli vibhag",
    "bijli connection",
    "vidyut vibhag",
    "police karyawahi",
    "giraftari",
    "adhikari se sampark"
]


def check_urgency(text_lower):
    # Search for urgency trigger words
    found = []
    for word in URGENCY_KEYWORDS:
        if word in text_lower:
            found.append(word)
    return found


def check_credentials(text_lower):
    # Search for requests asking for passwords, OTPs, or PINs
    found = []
    
    # Check if this is a standard safety warning (e.g. "Never share OTP" or "kabhi share na kare")
    is_safety_warning = (
        "never share" in text_lower or 
        "do not share" in text_lower or 
        "kisi ko na bataye" in text_lower or
        "share na kare" in text_lower
    )
    
    for word in CREDENTIAL_KEYWORDS:
        if word in text_lower:
            # If the message says "do not share OTP", it's a legitimate warning, not a scam request
            if "otp" in word and is_safety_warning:
                continue
            found.append(word)
    return found


def check_rewards(text_lower):
    # Search for prize and lottery promises
    found = []
    for word in REWARD_KEYWORDS:
        if word in text_lower:
            found.append(word)
    return found


def check_authority(text_lower):
    # Search for authority intimidation or service threats
    found = []
    for word in AUTHORITY_KEYWORDS:
        if word in text_lower:
            found.append(word)
    return found


def analyze_rules(message_text, language="en", *args, **kwargs):
    # Convert message to lowercase so matching is case-insensitive
    text_lower = message_text.lower()
    
    # A list of clear, human-readable explanations of every red flag found
    red_flag_reasons = []
    
    # Total red flag count
    flag_count = 0
    
    is_hindi = (language == "hi")
    
    # 1. Run Urgency Check
    urgent_matches = check_urgency(text_lower)
    if len(urgent_matches) > 0:
        words_found = ", ".join(urgent_matches)
        if is_hindi:
            red_flag_reasons.append(f"जल्दबाजी या धमकी (Urgency/Threat): डराने वाले शब्द मिले ({words_found}).")
        else:
            red_flag_reasons.append(f"Artificial urgency/threat detected: contains panic words ({words_found}).")
        flag_count += len(urgent_matches)
        
    # 2. Run Credentials Check
    credential_matches = check_credentials(text_lower)
    if len(credential_matches) > 0:
        words_found = ", ".join(credential_matches)
        if is_hindi:
            red_flag_reasons.append(f"संवेदनशील जानकारी की मांग (Credential Request): गोपनीय पिन या ओटीपी मांगा गया ({words_found}).")
        else:
            red_flag_reasons.append(f"High-risk credential request: asks for sensitive items like ({words_found}).")
        flag_count += len(credential_matches) * 2  # Higher weight for credential requests
        
    # 3. Run Reward / Prize Check
    reward_matches = check_rewards(text_lower)
    if len(reward_matches) > 0:
        words_found = ", ".join(reward_matches)
        if is_hindi:
            red_flag_reasons.append(f"लॉटरी या पैसे का लालच (Financial Bait): इनाम या फर्जी रिफंड का लालच ({words_found}).")
        else:
            red_flag_reasons.append(f"Financial bait detected: offers prizes, lotteries, or easy money ({words_found}).")
        flag_count += len(reward_matches)
        
    # 4. Run Authority Impersonation Check
    authority_matches = check_authority(text_lower)
    if len(authority_matches) > 0:
        words_found = ", ".join(authority_matches)
        if is_hindi:
            red_flag_reasons.append(f"अधिकारी या विभाग का फर्जी नाम (Authority Pressure): सरकारी या बिजली विभाग का नाम लिया ({words_found}).")
        else:
            red_flag_reasons.append(f"Authority pressure detected: mentions official entities or actions ({words_found}).")
        flag_count += len(authority_matches)
        
    # 5. Check Links using url_checker.py
    url_report = analyze_urls_in_message(message_text)
    if len(url_report["reasons"]) > 0:
        for reason in url_report["reasons"]:
            if is_hindi:
                red_flag_reasons.append(f"खतरनाक लिंक (Unsafe Link): {reason}")
            else:
                red_flag_reasons.append(f"Link safety issue: {reason}")
        flag_count += len(url_report["reasons"]) * 2  # Higher weight for suspicious links
        
    # Return a comprehensive rule summary
    return {
        "flag_count": flag_count,
        "reasons": red_flag_reasons,
        "has_red_flags": len(red_flag_reasons) > 0,
        "url_report": url_report
    }
