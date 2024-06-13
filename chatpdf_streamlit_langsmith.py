from langchain_community.document_loaders import PyPDFLoader
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.chains import ChatVectorDBChain
from langchain.chains import RetrievalQA
from langchain_community.llms import Cohere
import streamlit as st
import os
from langsmith import Client
import langsmith
from langchain import smith
from langchain.smith import RunEvalConfig

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__970d62ad405a4415a471223e7ea4e6d9"


########################################## Indexing ####################################################
pdf_loader = PyPDFDirectoryLoader("./docs")
loaders= [pdf_loader]

documents = []
for loader in loaders :
    documents.extend(loader.load())

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=100)
all_documents = text_splitter.split_documents(documents)

print(f"Total no of documents:{len(all_documents)}")

embeddings = CohereEmbeddings(cohere_api_key='eJsSh3EXHErcxdR2T6atI2b9GEF1QFlnO6PqJM0B')
vectordb = Chroma.from_documents(all_documents, embedding=embeddings, persist_directory="./chroma_db")

vectordb.persist()

################################## LLM body ############################################################
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
llm = Cohere(cohere_api_key='eJsSh3EXHErcxdR2T6atI2b9GEF1QFlnO6PqJM0B')

memory = ConversationBufferMemory(llm=llm, memory_key="chat_history", return_documents=True, output_key="answer")

# pdf_qa = ChatVectorDBChain.from_llm(
#     Cohere(cohere_api_key='eJsSh3EXHErcxdR2T6atI2b9GEF1QFlnO6PqJM0B'),
#     vectordb,
#     return_source_documents=True,
# )
retv=db.as_retriever(search_kwargs={"k":3})
pdf_qa = RetrievalQA.from_chain_type(llm=llm, retriever=retv)

eval_config = smith.RunEvalConfig(
    evaluators=[
        "cot_qa",
        RunEvalConfig.Criteria("relevance"),
    ],
    custom_evaluators=[],
    eval_llm=llm
)

client = Client()
chain_results = client.run_on_dataset(
    dataset_name="3gpp_29series_dataset",
    llm_or_chain_factory=pdf_qa,
    evaluation=eval_config,
    concurrency_level=5,
    verbose=True,
)
# Streamlit app
st.title("PDF chat App")

# User input based on your model's task
query = st.text_input("Enter your text here")
if query:
    result = pdf_qa({"query": query})

    st.write("**Model Output:**")
    #st.json(result)  # Display predictions in JSON format

    generated_text = result["result"]
    st.write(f"Response: {generated_text}")