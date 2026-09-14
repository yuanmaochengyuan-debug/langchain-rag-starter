import requests
import streamlit as st


API_URL = "http://localhost:8000/api/v1/query"


st.set_page_config(
    page_title="RAG Demo",
    page_icon="🔍",
)

st.title("🔍 LangChain RAG Starter")
st.caption("Ask questions about your documents")


question = st.text_input(
    "Your question:",
    placeholder="What is this document about?",
)


if st.button("Ask", use_container_width=True) and question:
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

            st.markdown("### Answer")
            st.write(data["answer"])

            sources = data.get("sources", [])

            if sources:
                st.markdown("### Sources")

                for index, src in enumerate(sources, start=1):
                    file_name = src.get("file", "unknown")
                    page = src.get("page")
                    snippet = src.get("snippet", "")

                    if page is not None:
                        title = f"📄 Source {index}: {file_name} · Page {page}"
                    else:
                        title = f"📄 Source {index}: {file_name}"

                    with st.expander(title):
                        st.write(snippet)

        except requests.RequestException as e:
            st.error(f"API request failed: {e}")

        except Exception as e:
            st.error(f"Error: {e}")