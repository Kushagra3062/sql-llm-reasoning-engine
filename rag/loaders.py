from langchain_community.document_loaders import WebBaseLoader, WikipediaLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_documents():
    print("[RAG] Loading documents from News URLs and Wikipedia...")
    urls = [
        "https://www.reuters.com/markets/",
        "https://www.cnbc.com/technology/",
        "https://finance.yahoo.com/news/"
    ]
    
    docs = []
    
    # Load Web Docs
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            docs.extend(loader.load())
        except Exception as e:
            print(f"[RAG] Failed to load {url}: {e}")
            
    # Load Wikipedia (Apple & Microsoft as defaults or examples)
    try:
        wiki_loader = WikipediaLoader(query="Apple Inc.", load_max_docs=1)
        docs.extend(wiki_loader.load())
        wiki_loader2 = WikipediaLoader(query="Microsoft", load_max_docs=1)
        docs.extend(wiki_loader2.load())
    except Exception as e:
        print(f"[RAG] Failed to load Wikipedia: {e}")

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    print(f"[RAG] Generated {len(splits)} document chunks.")
    return splits
