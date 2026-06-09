import streamlit as st
import requests
import json

# Use the secure secret
API_KEY = st.secrets["GEMINI_API_KEY"]
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

st.set_page_config(page_title="LC Troubleshooter", layout="centered")
st.title("LC Troubleshooter")

system = st.selectbox("System", ["Waters Acquity UPLC", "Agilent 1260 HPLC", "Agilent 1290 UHPLC", "Other"])
part_num = st.text_input("Column Part #")
mpa = st.text_input("Mobile Phase A (e.g. 95% Water + 0.1% FA)")
mpb = st.text_input("Mobile Phase B (e.g. 5% ACN)")
issue = st.text_area("Describe the Issue")

if st.button("Troubleshoot"):
    with st.spinner("Analyzing..."):
        prompt = f"Troubleshoot this LC issue: {issue}. System: {system}, Column P/N: {part_num}, MP A: {mpa}, MP B: {mpb}. Return 3-5 physical checklist items."
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            response = requests.post(URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
            data = response.json()
            st.write(data['candidates'][0]['content']['parts'][0]['text'])
        except Exception as e:
            st.error(f"Error: {e}")
