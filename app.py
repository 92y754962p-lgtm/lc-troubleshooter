import streamlit as st
import requests
import json

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
        # Fetch the key from Streamlit's secure storage
        API_KEY = st.secrets["GEMINI_API_KEY"]
        URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
"
        
        with st.spinner("Analyzing..."):
            prompt = f"Troubleshoot this LC issue: {issue}. System: {system}, Column P/N: {part_num}, MP A: {mpa}, MP B: {mpb}. Return 3-5 physical checklist items."
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            data = response.json()
            
            # Check for valid data
            if 'candidates' in data and len(data['candidates']) > 0:
                st.write(data['candidates'][0]['content']['parts'][0]['text'])
            elif 'error' in data:
                st.error(f"API Error: {data['error']['message']}")
            else:
                st.error(f"Unexpected response: {data}")
    except KeyError:
        st.error("API Key missing! Make sure 'GEMINI_API_KEY' is saved in your Streamlit Cloud 'Secrets' settings.")
    except Exception as e:
        st.error(f"Error: {e}")
