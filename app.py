import streamlit as st
import requests
import json
import time

# App configuration
st.set_page_config(page_title="LC Troubleshooter", layout="centered")
st.title("LC Troubleshooter")

# UI Inputs
system = st.selectbox("System", ["Waters Acquity UPLC", "Agilent 1260 HPLC", "Agilent 1290 UHPLC", "Other"])
part_num = st.text_input("Column Part #")
mpa = st.text_input("Mobile Phase A (e.g. 95% Water + 0.1% FA)")
mpb = st.text_input("Mobile Phase B (e.g. 5% ACN)")
issue = st.text_area("Describe the Issue")

if st.button("Troubleshoot"):
    try:
        # Securely fetch API key
        API_KEY = st.secrets["GEMINI_API_KEY"]
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={API_KEY}"
        
        with st.spinner("Analyzing..."):
            prompt = f"Troubleshoot this LC issue: {issue}. System: {system}, Column P/N: {part_num}, MP A: {mpa}, MP B: {mpb}. Return 3-5 physical checklist items."
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            # Retry logic for 503 errors
            response = None
            for i in range(3):
                response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
                if response.status_code != 503:
                    break
                time.sleep(2) # Wait 2 seconds before retrying
            
            data = response.json()
            
            # Check response structure
            if 'candidates' in data and len(data['candidates']) > 0:
                result = data['candidates'][0]['content']['parts'][0]['text']
                st.write(result)
            elif 'error' in data:
                st.error(f"API Error ({response.status_code}): {data['error']['message']}")
            else:
                st.error(f"Unexpected response format: {data}")
                
    except KeyError:
        st.error("API Key missing! Ensure 'GEMINI_API_KEY' is set in Streamlit Cloud Secrets.")
    except Exception as e:
        st.error(f"Error: {e}")
