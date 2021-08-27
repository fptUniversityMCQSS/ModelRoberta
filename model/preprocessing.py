import os
from dotenv import load_dotenv
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor import PreProcessor
from model.retriever import retriever
from haystack.file_converter.txt import TextConverter
from haystack.document_store import MilvusDocumentStore
# from haystack.utils import launch_es

# Load environment docker for elasticsearch
# launch_es()

# Load environment sqlite

load_dotenv()

'''encode documents'''


def preprocess(dir_file, pattern, delete_all_document):

    load_docs = load_document(dir_file, pattern)

    # Optimize and write down to database (SQLite3)
    # if you want to delete all document_store before : delete_all_document = True

    document_store = load_document_store(
        delete_all_document=delete_all_document)

    # Write down processed document into database and update embeddings
    document_store.write_documents(load_docs)
    # document_store = store_documents(load_docs, delete_all_document=delete_all_document)

    retrieve = retriever(document_store)

    document_store.update_embeddings(retrieve)

    return "Encode Successful"


def load_document(dir_file, pattern):

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=True,
        split_by='word',
        split_length=300,
        split_respect_sentence_boundary=True,
        split_overlap=0,
    )

    if pattern == "folder":
        all_docs = convert_files_to_dicts(
            dir_path=dir_file, clean_func=clean_wiki_text, split_paragraphs=True)
        nested_docs = [preprocessor.process(d) for d in all_docs]
        docs = [d for x in nested_docs for d in x]
        return docs

    converter = TextConverter(remove_numeric_tables=True)
    doc_txt = converter.convert(file_path=dir_file, meta=None)
    docs = preprocessor.process(doc_txt)
    return docs
    
def load_document_store(delete_all_document):
    
    document_store = MilvusDocumentStore(
        sql_url=os.getenv('PROCESSED_DOCUMENTS_DB'),
        milvus_url="tcp://localhost:19530",
        connection_pool="SingletonThread",
        similarity="dot_product",
        return_embedding=True,
        embedding_field="embedding",
        duplicate_documents="overwrite",
    )
    if delete_all_document == True:
        document_store.delete_all_documents()

    return document_store



'''
def store_documents(load_docs, delete_all_document):
    """
        To store preprocessed document into database
        To install sqlite3 on Ubuntu, type:
            $ sudo apt install sqlite3
        Then
            $ sqlite3 data/processed_documents.db
        Enter `.tables` inside SQLite3 prompt then Ctrl + D
    """

    document_store = FAISSDocumentStore(
        sql_url=os.getenv('PROCESSED_DOCUMENTS_DB'),
        faiss_index_factory_str='Flat',
        vector_dim=768,
        return_embedding=True,
        similarity='dot_product',
        index='document',
        duplicate_documents='overwrite',
        )

    if delete_all_document == True:
        document_store.delete_all_documents()

    # Write down processed document into database
    document_store.write_documents(load_docs, index='document')

    return document_store
'''
