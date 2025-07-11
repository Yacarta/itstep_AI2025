import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
import dotenv
import os
from uuid import uuid4

# Load environment variables
dotenv.load_dotenv()

# Get API keys
api_key = os.getenv('GEMINI_API_KEY')
pinecone_api_key = os.getenv('PINECONE_API_KEY')

# Initialize embeddings model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    google_api_key=api_key
)

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index_name = "itstep"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(index_name)
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# Streamlit app
st.title("Завантаження документів")

# Document upload section
st.header("Система для завантаження")
uploaded_files = st.file_uploader(
    "Оберіть файли для завантаження",
    type=["txt", "pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    documents = []
    for uploaded_file in uploaded_files:
        file_content = uploaded_file.read().decode("utf-8")

        doc = Document(
            page_content=file_content,
            metadata={
                'filename': uploaded_file.name,
                'type': "uploaded",
                'author': "User"
            }
        )
        documents.append(doc)

    if st.button("Завантажити у векторну базу"):
        if documents:
            ids = [str(uuid4()) for _ in range(len(documents))]
            vector_store.add_documents(documents, ids=ids)
            st.success(f"Завантажено {len(documents)} документів!")

# Search section
st.header("Пошук документів")
user_query = st.text_input("Введіть запит:")

if user_query:
    search_filter = None
    docs = vector_store.similarity_search(
        user_query,
        k=2,
        filter=search_filter
    )


    st.subheader("Результати пошуку")
    if not docs:
        st.write("Немає таких документів.")
    else:
        for i, doc in enumerate(docs, 1):
            st.write(f"### Результати {i}")
            st.write(doc.page_content)
            st.write("**Metadata:**", doc.metadata)
            st.write("---")