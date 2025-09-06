import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="Insurance Policy Chatbot",
    page_icon="🤖",
    layout="wide",
)

# --- Application Title and Description ---
st.title("Insurance Policy Generation Chatbot")
st.markdown(
    """
    This application uses a Retrieval-Augmented Generation (RAG) pipeline to create
    insurance policies based on your needs. The backend is built with FastAPI and Haystack,
    and it draws information from a knowledge base of sample insurance documents.

    **To get started:**
    1. Enter a description of the policy you want in the text box below.
    2. Click the "Generate Policy" button.
    3. The system will retrieve relevant information and generate a policy.

    *(Note: The LLM generator is optional. If not configured, the app will show the documents retrieved from the knowledge base.)*
    """
)

# --- User Input Area ---
with st.form("policy_form"):
    query = st.text_area(
        "**Describe the insurance policy you need:**",
        height=150,
        placeholder="e.g., 'Generate a standard auto insurance policy for a driver with one at-fault accident.'"
    )
    submit_button = st.form_submit_button("Generate Policy")

# --- Policy Generation Logic ---
if submit_button and query:
    with st.spinner("Generating your policy... This may take a moment."):
        try:
            # The FastAPI backend service is named 'backend' in docker-compose
            api_url = "http://backend:8000/generate_policy"

            response = requests.post(api_url, json={"query": query}, timeout=60)
            response.raise_for_status()  # Raise an exception for HTTP errors

            result = response.json()

            st.divider()
            st.subheader("📜 Generated Policy")
            st.markdown(result.get("policy", "No policy was generated."))

            st.divider()
            st.subheader("🧠 Retrieved Documents")
            st.info(
                "These are the top documents retrieved from the knowledge base that were used as context for the generation."
            )

            retrieved_documents = result.get("retrieved_documents", [])
            if retrieved_documents:
                for i, doc in enumerate(retrieved_documents):
                    with st.expander(f"**Document {i+1}** (Score: {doc['score']:.2f})"):
                        st.markdown(doc.get("content", "No content available."))
                        st.write("---")
                        st.json(doc.get("meta", {}))
            else:
                st.warning("No documents were retrieved from the knowledge base.")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the backend API. Please ensure the backend service is running. Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

elif submit_button:
    st.warning("Please enter a description for the policy you need.")
