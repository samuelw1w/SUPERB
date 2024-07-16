import os
import logging
import sys
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, StorageContext, load_index_from_storage, KnowledgeGraphIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.core import Settings
from llama_index.readers.file import HTMLTagReader, CSVReader, DocxReader, EpubReader, FlatReader, HWPReader, IPYNBReader, ImageCaptionReader, ImageReader, ImageTabularChartReader, ImageVisionLLMReader, MarkdownReader, MboxReader, PDFReader, PagedCSVReader, PandasCSVReader, PptxReader, PyMuPDFReader, VideoAudioReader, XMLReader
from llama_index.core.callbacks import CallbackManager
#from llama_index.callbacks.uptrain.base import UpTrainCallbackHandler


# Setup logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
os.environ['OPENAI_API_KEY'] = 'add-api-key-here'

# Load OpenAI API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logging.error("OPENAI_API_KEY not found in environment variables.")
    exit(1)

# Create a ServiceContext
Settings.llm = OpenAI(temperature=0, model="gpt-4o")
Settings.node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=20)
Settings.embed_model = OpenAIEmbedding()

# Initialize VectorStoreIndex and load or create index
def construct_index(directory_path):
    try:        
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    except:
        documents = SimpleDirectoryReader(directory_path).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist()
    return index

index = construct_index("html_downloads")

# Define queries and get responses from the chatbot using the context information
queries = [
    "Describe what a database is",
    # Add more queries as needed
]

for query in queries:
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    logging.info(f"Query: {query}\nResponse: {response}")