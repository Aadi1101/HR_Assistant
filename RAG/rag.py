from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_vector_database(txt_path):
    loader = TextLoader(txt_path)
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        separators="\n",
        chunk_overlap = 200
    ).split_documents(docs)
    embedding = HuggingFaceEmbeddings()
    db = FAISS.from_documents(documents=documents,embedding=embedding)
    db.save_local("./faiss-db")

if __name__ == '__main__':
    create_vector_database("NewJoiners.txt")