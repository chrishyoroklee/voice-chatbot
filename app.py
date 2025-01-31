import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader

# Function to load and process the PDF
def load_db(file_path, chain_type, k, openai_api_key):
    # Load documents
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    # Define embedding
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Create vector database
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)

    # Define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})

    # Create chatbot chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key),
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa

# Streamlit App
def main():
    st.title("ChatWithYourData_Bot")

    # Sidebar for API key input
    with st.sidebar:
        st.header("Configuration")
        openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
        st.markdown("**Note:** Your API key is not stored and is only used for this session.")

    # Check if API key is provided
    if not openai_api_key:
        st.warning("Please enter your OpenAI API key to proceed.")
        return

    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Initialize session state for chat history and QA chain
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "qa" not in st.session_state:
        st.session_state.qa = None

    # Load PDF and initialize QA chain
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            # Save the uploaded file temporarily
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Load and process the PDF
            st.session_state.qa = load_db("temp.pdf", "stuff", 4, openai_api_key)
            st.success("PDF processed and ready for queries!")

    # Chat interface
    st.header("Chat with your PDF")
    user_query = st.text_input("Enter your question:")

    if user_query and st.session_state.qa:
        # Get response from the QA chain
        result = st.session_state.qa({"question": user_query, "chat_history": st.session_state.chat_history})

        # Update chat history
        st.session_state.chat_history.append((user_query, result["answer"]))

        # Display the answer
        st.markdown(f"**ChatBot:** {result['answer']}")

        # Display source documents (if needed)
        with st.expander("Source Documents"):
            for doc in result["source_documents"]:
                st.write(doc)

    # Display chat history
    st.header("Chat History")
    for i, (query, answer) in enumerate(st.session_state.chat_history):
        st.markdown(f"**User:** {query}")
        st.markdown(f"**ChatBot:** {answer}")
        st.markdown("---")

    # Clear chat history button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")

# Run the app
if __name__ == "__main__":
    main()