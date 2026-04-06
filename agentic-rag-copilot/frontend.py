import streamlit as st
import requests

st.set_page_config(page_title="RAG Copilot", layout="centered")

st.title("🧠 Agentic RAG Copilot")

query = st.text_input("Ask something")

if st.button("Submit") and query.strip():
    with st.spinner("Thinking..."):
        try:
            res = requests.post(
                "http://localhost:8000/ask",
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=60
            )

            if res.status_code == 200:
                data = res.json()

                if "answer" in data:
                    st.markdown("### ✅ Answer")
                    st.markdown(data["answer"])
                else:
                    st.error(data.get("error", "Unknown error"))

            else:
                st.error(f"Request failed with status {res.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {e}")