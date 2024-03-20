from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma



def doc_to_vectorstore(docs, company_name):
    output_dir=company_name+"_chroma_db"
    embedding_function = SentenceTransformerEmbeddings(
          model_name="all-MiniLM-L6-v2")
    #db = Chroma.from_documents(docs, embedding_function)

    db = Chroma.from_documents(docs, embedding_function, persist_directory=output_dir)
    return db