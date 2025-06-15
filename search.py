from database import collection 

def find_final_version(chapter_id: str):
    """
    Finds the final, 'approved' version of a chapter using metadata filtering.
    This is the most reliable way to retrieve the correct final document.
    """
    print(f"\n--- Searching for the 'approved' version of '{chapter_id}'... ---")
    try:
        results = collection.get(
            where={
                "$and": [
                    {'chapter_id': {'$eq': chapter_id}},
                    {'status': {'$eq': 'approved'}}
                ]
            },
            limit=1 # We only expect one approved version
        )
        print(results)
        print("----\n", results['documents'])
        if results and results['documents']:
            print("--- ✅ Final version found in database! ---")
            return results['documents'][0]
        else:
            print("--- ⚠️ No 'approved' version found for this chapter yet. ---")
            return None
    except Exception as e:
        print(f"An error occurred during search: {e}")
        return None

def semantic_search_versions(chapter_id: str, query_text: str, n_results: int = 3):
    """
    Performs a semantic search to find the most relevant versions of a chapter
    based on a text query.
    """
    print(f"\n--- Performing semantic search for query: '{query_text}'... ---")
    try:
        results = collection.query(
            query_texts=[query_text],
            where={"chapter_id": {'$eq': chapter_id}}, 
            n_results=n_results
        )
        
        if results and results['documents']:
            print("--- ✅ Semantic search complete! Found relevant versions. ---")
            return results
        else:
            print("--- ⚠️ No relevant versions found for this query. ---")
            return None
    except Exception as e:
        print(f"An error occurred during semantic search: {e}")
        return None