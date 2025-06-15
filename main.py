from config import Config
from scraper import fetch_and_clean
from agents import ai_writer_spin_chapter, ai_reviewer_critique, ai_writer_spin_with_feedback
from utils.cache_handler import get_cached_content, save_content_to_cache
from database import save_version, get_latest_version_info, inspect_all_versions
from search import find_final_version, semantic_search_versions


CONFIG = Config()
URL = CONFIG.url
CONTENT_SELECTOR = CONFIG.content_selector
CHAPTER_ID = "gates_of_morning_ch1" 



def handle_spin_cycle(original_text: str, current_text: str, current_version_num: int):
    """Manages a single "spin" cycle and returns the new state."""
    print("\n--- Generating new AI draft... ---")
    spun_text = ai_writer_spin_chapter(current_text)
    current_version_num += 1
    save_version(chapter_id=CHAPTER_ID, version_num=current_version_num, status="ai_draft", text=spun_text)
    
    review_text = ai_reviewer_critique(original_text, spun_text)
    
    print("\n" + "="*50)
    print(f"---  REVIEW OF DRAFT v{current_version_num} ---")
    print(f"\n---  AI REVIEWER'S FEEDBACK ---\n{review_text}")
    print(f"\n---  AI WRITER'S DRAFT ---\n{spun_text}")
    print("="*50 + "\n")

    print("--- HUMAN ACTION REQUIRED ---")
    print("First, as a REVIEWER, assess the AI's critique.")
    human_review_feedback = input("--> Do you agree with the review? (Press Enter to accept, or type concerns): ").strip()
    
    print("\nNow, as an EDITOR, provide creative direction.")
    human_editor_feedback = input("--> Your command: [approve], [retry], or provide feedback for the writer: ").strip().lower()

    if human_editor_feedback == 'approve':
        save_version(chapter_id=CHAPTER_ID, version_num=current_version_num, status="approved", text=spun_text)
        print("\n---  Chapter Approved! Final version saved. ---")
        return spun_text, current_version_num # Return the approved state
    
    elif human_editor_feedback == 'retry':
        print("\n---  discarding current draft. Using previous version for next spin... ---")
        # Return the original text and decremented version number to retry
        return current_text, current_version_num - 1
    
    else:
        combined_feedback = f"Editor's creative direction: '{human_editor_feedback}'."
        if human_review_feedback:
            combined_feedback += f" Also, please address this meta-concern about the review: '{human_review_feedback}'."
        
        print("\n--- Sending combined human feedback to AI Writer for refinement... ---")
        # Return the newly refined text as the new 'current_text'
        return ai_writer_spin_with_feedback(spun_text, combined_feedback), current_version_num

def handle_search():
    """Manages the search functionality submenu."""
    print("\n--- Search Menu ---")
    search_type = input("Search for [final] approved version or perform a [semantic] search? ").lower().strip()
    
    if search_type == 'final':
        final_doc = find_final_version(CHAPTER_ID)
        if final_doc:
            print(f"\n--- Retrieved Final Approved Chapter ---\n{final_doc[:500]}...")
    
    elif search_type == 'semantic':
        query = input("Enter your search query (e.g., 'a description of the morning room'): ")
        search_results = semantic_search_versions(CHAPTER_ID, query)
        if search_results and search_results['documents']:
            print("\n--- Top Semantic Search Results ---")
            for i, doc in enumerate(search_results['documents'][0]):
                meta = search_results['metadatas'][0][i]
                dist = search_results['distances'][0][i]
                print(f"\n--- Result {i+1} (v{meta['version']}, Status: {meta['status']}, Distance: {dist:.4f}) ---")
                print(f"{doc[:300]}...")
    else:
        print("Invalid search type.")


# --- Main Application Workflow ---
def main():
    """The main entry point and interactive loop for the application."""
    print(f"--- Initializing content for URL: {URL} ---")
    original_text = get_cached_content(URL) or fetch_and_clean(URL, CONTENT_SELECTOR)
    if not original_text or "FAILED" in original_text:
        print("CRITICAL: Halting workflow due to scraping failure.")
        return
    save_content_to_cache(URL, original_text) # Ensure cache is always updated
    
    save_version(chapter_id=CHAPTER_ID, version_num=0, status="original", text=original_text)
    
    current_text, current_version_num = get_latest_version_info(chapter_id=CHAPTER_ID)
    
    print("\n" + "="*50)
    print(" Automated Book Workflow is Ready ")
    print(f"Loaded Chapter: '{CHAPTER_ID}', starting at Version {current_version_num}")
    print("="*50)

    while True:
        print("\nAvailable Commands: [spin], [search], [inspect], [exit]")
        command = input("➡️ Your command: ").lower().strip()

        if command == "exit":
            print("Exiting application. Goodbye!")
            break
        elif command == "spin":
            current_text, current_version_num = handle_spin_cycle(original_text, current_text, current_version_num)
        elif command == "search":
            handle_search()
        elif command == "inspect":
            inspect_all_versions(CHAPTER_ID)
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
    print("\n--- Workflow session ended. ---")