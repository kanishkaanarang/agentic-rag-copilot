import streamlit as st
import requests

query = st.text_input("Ask something")

if st.button("Submit"):
    res = requests.post(
        "http://localhost:8000/ask",
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )

    st.write("Status:", res.status_code)

    try:
        st.write(res.json())
    except:
        st.write("Raw response:", res.text)