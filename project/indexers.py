# indexers.py
from pathlib import Path
from haystack.components.converters import PyPDFToDocument, CSVToDocument
from haystack.document_stores.in_memory import InMemoryDocumentStore

def index_pdf_documents(directory: Path, document_store: InMemoryDocumentStore):
    """
    Converts all PDFs in the directory to Documents and writes them to the document store.
    """
    converter = PyPDFToDocument()
    documents = []
    for pdf_file in directory.glob('*.pdf'):
        result = converter.run(sources=[pdf_file])
        docs = result.get('documents', [])
        for doc in docs:
            doc.meta['filename'] = pdf_file.name
        documents.extend(docs)
    document_store.write_documents(documents)

def index_csv_documents(directory: Path, document_store: InMemoryDocumentStore):
    """
    Converts all CSVs in the directory to Documents and writes them to the document store.
    """
    converter = CSVToDocument()
    documents = []
    for csv_file in directory.glob('*.csv'):
        result = converter.run(sources=[csv_file])
        docs = result.get('documents', [])
        for doc in docs:
            doc.meta['filename'] = csv_file.name
        documents.extend(docs)
    document_store.write_documents(documents)