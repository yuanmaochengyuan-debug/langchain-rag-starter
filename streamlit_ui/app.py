import streamlit as st
import requests

API_URL = "http://localhost:8000/api/v1/query"

st.set_page_config(page_title="RAG Demo", page_icon="🔍")
st.title("🔍 LangChain RAG Starter")
st.caption("Ask questions about your uploaded documents")

question = st.text_input("Your question:", placeholder="What is this document about?")

if st.button("Ask", use_container_width=True) and question:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, json={"question": question})
            data = response.json()
            st.markdown("### Answer")
            st.write(data["answer"])
            if data["sources"]:
                st.markdown("### Sources")
                for src in data["sources"]:
                    st.caption(f"📄 {src}")
        except Exception as e:
            st.error(f"Error: {e}")