# url_checker.py - Detects suspicious links inside SMS and WhatsApp messages

import re
from urllib.parse import urlparse

# List of known URL shorteners that hide the real destination website
SHORTENER_DOMAINS = [
    "bit.ly",
    "tinyurl.com",
    "is.gd",
    "t.co",
    "ow.ly",
    "buff.ly",
    "cutt.ly"
]

# List of low-cost domain extensions frequently used in phishing scams
SUSPICIOUS_EXTENSIONS = [
    ".xyz",
    ".top",
    ".club",
    ".click",
    ".site",
    ".biz",
    ".info"
]

# Sensitive Indian brands and services that scammers frequently imitate
SENSITIVE_BRANDS = [
    "sbi",
    "hdfc",
    "icici",
    "paytm",
    "phonepe",
    "gpay",
    "jio",
    "airtel",
    "pan",
    "aadhaar",
    "incometax"
]


def extract_urls(message_text):
    # Regular expression pattern to find web addresses starting with http://, https://, or www.
    url_pattern = r'(https?://[^\s]+|www\.[^\s]+)'
    
    # Find all matching links in the text
    found_urls = re.findall(url_pattern, message_text)
    
    # Return the list of found URLs
    return found_urls


def check_single_url(url):
    # Keep track of suspicious reasons found for this specific link
    reasons = []
    
    # Make sure URL has a protocol so urlparse works properly
    if not url.startswith("http://") and not url.startswith("https://"):
        test_url = "http://" + url
    else:
        test_url = url
        
    # Break the URL into components like domain, path, etc.
    parsed = urlparse(test_url)
    domain_name = parsed.netloc.lower()
    
    # 1. Check if the link uses an IP address instead of a domain name (e.g., http://192.168.1.1)
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    if re.match(ip_pattern, domain_name):
        reasons.append(f"Uses a raw numeric IP address ({domain_name}) instead of a trusted website domain name.")
        
    # 2. Check if the link uses a URL shortener
    for shortener in SHORTENER_DOMAINS:
        if shortener in domain_name:
            reasons.append(f"Uses a URL shortener service ({shortener}) that hides the true destination.")
            break
            
    # 3. Check for suspicious or low-cost domain endings
    for extension in SUSPICIOUS_EXTENSIONS:
        if domain_name.endswith(extension):
            reasons.append(f"Uses a domain extension ({extension}) that is commonly seen in scam websites.")
            break
            
    # 4. Check if a sensitive bank or brand name appears in a non-official domain
    for brand in SENSITIVE_BRANDS:
        if brand in domain_name:
            # Trusted domains for these brands normally end with .com or .in without hyphens
            trusted_officials = [
                f"{brand}.com",
                f"{brand}.co.in",
                f"{brand}.in",
                "onlinesbi.sbi",
                "incometax.gov.in"
            ]
            
            # Check if this domain is exactly one of the official ones
            is_official = False
            for official in trusted_officials:
                if domain_name == official or domain_name.endswith("." + official):
                    is_official = True
                    break
                    
            # If brand is in the domain name but it is not an official site, flag it
            if not is_official:
                reasons.append(f"Contains the brand '{brand}' inside an unofficial domain ({domain_name}).")
                break
                
    return reasons


def analyze_urls_in_message(message_text):
    # Extract all links from the message
    urls = extract_urls(message_text)
    
    # Store all findings
    all_reasons = []
    
    # If no links are found, return empty results
    if len(urls) == 0:
        return {
            "has_urls": False,
            "url_count": 0,
            "urls_found": [],
            "reasons": []
        }
        
    # Check each extracted link one by one
    for link in urls:
        link_reasons = check_single_url(link)
        for reason in link_reasons:
            all_reasons.append(reason)
            
    # Return structured information about the message's links
    return {
        "has_urls": True,
        "url_count": len(urls),
        "urls_found": urls,
        "reasons": all_reasons
    }
