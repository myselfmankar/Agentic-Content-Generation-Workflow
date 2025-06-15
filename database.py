import chromadb
from chromadb.utils import embedding_functions
import pandas as pd


client = chromadb.PersistentClient(path="db")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


collection = client.get_or_create_collection(
    name="book_versions",
    embedding_function=embedding_function,
    metadata={"hnsw:space": "cosine"} # Use cosine similarity for searching
)

def save_version(chapter_id: str, version_num: int, status: str, text: str):
    """
    Saves a version of the text to ChromaDB with structured metadata.
    """
    # Create a unique ID for this specific document
    doc_id = f"{chapter_id}_v{version_num}"
    
    print(f"--- Saving to DB: ID='{doc_id}', Status='{status}' ---")
    
    try:
        collection.upsert(
            documents=[text],
            metadatas=[{
                "chapter_id": chapter_id,
                "version": version_num,
                "status": status # e.g., "original", "ai_draft", "human_edited", "approved"
            }],
            ids=[doc_id]
        )
    except Exception as e:
        print(f"--- ERROR: Failed to save version to ChromaDB: {e} ---")

def get_latest_version_info(chapter_id: str):
    """
    Retrieves the text and version number of the highest version for a chapter.
    """
    try:
        results = collection.get(where={"chapter_id": {'$eq': chapter_id}})
        
        if not results['ids']:
            return None, -1 # No version found

        # Find the highest version number from the metadata
        latest_version = -1
        latest_doc = ""
        for i, meta in enumerate(results['metadatas']):
            if meta['version'] > latest_version:
                latest_version = meta['version']
                latest_doc = results['documents'][i]
        
        return latest_doc, latest_version
    except Exception as e:
        print(f"ERROR: {e}")
        return None, -1
    

def inspect_all_versions(chapter_id: str):
    """
    Fetches all versions for a given chapter_id and displays them in a table.
    """
    print(f"\n--- Inspecting all versions for Chapter ID: '{chapter_id}' ---")
    try:
        # The get() method with a 'where' filter retrieves specific documents.
        results = collection.get(
            where={"chapter_id": chapter_id}
        )

        if not results or not results['ids']:
            print("No versions found for this chapter in the database.")
            return

        # Prepare data for a clean Pandas DataFrame display
        data_to_display = {
            "ID": results['ids'],
            "Version": [meta.get('version', 'N/A') for meta in results['metadatas']],
            "Status": [meta.get('status', 'N/A') for meta in results['metadatas']],
            "Content Snippet": [doc[:100] + "..." for doc in results['documents']]
        }
        
        df = pd.DataFrame(data_to_display)
        
        # Sort by version number for a logical display
        if 'Version' in df.columns:
            df = df.sort_values(by="Version").set_index("Version")

        # Print the DataFrame to the console
        # to_string() ensures the whole table is printed without truncation
        print(df.to_string())

    except Exception as e:
        print(f"--- ERROR: Could not inspect the database: {e} ---")