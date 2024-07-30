from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama 
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate

embedding = HuggingFaceEmbeddings()

vectorstore_faiss = FAISS.load_local('faiss-db',embeddings=embedding,allow_dangerous_deserialization=True)

llm = Ollama(model='mistral')

prompt_template = """You are an AI Assistant. Given the following context:
{context}

Answer the following question:
{question}

Assistant:"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type="stuff",
    retriever = vectorstore_faiss.as_retriever(
        search_type = "similarity", search_kwargs = {"k":6}
    ),
    verbose = True,
    return_source_documents = True,
    chain_type_kwargs={"prompt":prompt}
)

question = "How many applicants are expecting the salary in range of 10 to 20 lakhs ?"
response = qa.invoke({"query":question})
result = response["result"]
print(result)