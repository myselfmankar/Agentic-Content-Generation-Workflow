from config import Config
from scraper import fetch_and_clean
from agents import ai_writer_spin_chapter, ai_reviewer_critique, ai_writer_spin_with_feedback
from utils.cache_handler import get_cached_content, save_content_to_cache
from database import save_version, get_latest_version_info, inspect_all_versions
from search import find_final_version, semantic_search_versions

# --- Configuration Constants ---
CONFIG = Config()
URL = CONFIG.url
CONTENT_SELECTOR = CONFIG.content_selector
CHAPTER_ID = "gates_of_morning_ch1" 

# --- Helper Functions for User Interaction ---

def handle_spin_cycle(original_text: str, current_text: str, current_version_num: int):
    """
    Manages a complete, iterative "spin" cycle: AI generation, review,
    and a continuous human decision loop for a single draft.
    """
    print("\n--- Generating new AI draft... ---")
    spun_text = ai_writer_spin_chapter(current_text)
    current_version_num += 1
    save_version(chapter_id=CHAPTER_ID, version_num=current_version_num, status="ai_draft", text=spun_text)
    
    while True: 
        review_text = ai_reviewer_critique(original_text, spun_text)

        print("\n" + "="*60)
        print(f"---  REVIEW OF DRAFT v{current_version_num} ---")
        print("\n---  AI REVIEWER'S FEEDBACK ---\n" + review_text)
        print("\n---  AI WRITER'S DRAFT ---\n" + spun_text)
        print("="*60 + "\n")

        # --- THE DECISION POINT MENU ---
        print("What is your next action for this draft?")
        print("  [1] Approve this version as final.")
        print("  [2] Refine this draft with new feedback.")
        print("  [3] Discard this draft and re-spin from the previous version.")
        print("  [4] Save this draft and return to the main menu.")
        
        choice = input(" Enter your choice (1-4): ").strip()

        # --- DECISION LOGIC ---
        if choice == '1': # Approve
            save_version(chapter_id=CHAPTER_ID, version_num=current_version_num, status="approved", text=spun_text)
            print("\n--- ✅ Chapter Approved! Final version status updated in DB. ---")
            return spun_text, current_version_num

        elif choice == '2': # Refine
            feedback = input(" Provide your feedback for the writer: ").strip()
            if not feedback:
                print("--- No feedback provided. Please try again. ---")
                continue
            print("\n--- Sending feedback to AI Writer for refinement... ---")
            refined_text = ai_writer_spin_with_feedback(spun_text, feedback)
            
            # The refined text becomes the new 'spun_text' to be reviewed in the next loop.
            spun_text = refined_text 
            current_version_num += 1
            save_version(chapter_id=CHAPTER_ID, version_num=current_version_num, status="human_edited_draft", text=spun_text)
            
            continue

        elif choice == '3': # Discard and Retry
            print("\n---  Discarding current draft. You are back at the main menu. ---")
            print("--- Type 'spin' again to generate a new draft from the previous version. ---")
            return current_text, current_version_num - 1

        elif choice == '4': # Return to main menu
            print("\n--- Current draft saved. Returning to main menu. ---")
            return spun_text, current_version_num

        else:
            print("--- Invalid choice. Please enter a number between 1 and 4. ---")

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
        if search_results and search_results.get('documents'):
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
    save_content_to_cache(URL, original_text)
    
    save_version(chapter_id=CHAPTER_ID, version_num=0, status="original", text=original_text)
    
    current_text, current_version_num = get_latest_version_info(chapter_id=CHAPTER_ID)
    
    print("\n" + "="*50)
    print("🚀 Automated Book Workflow is Ready 🚀")
    print(f"Loaded Chapter: '{CHAPTER_ID}', starting at Version {current_version_num}")
    print("="*50)

    # The main loop now only manages high-level commands.
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