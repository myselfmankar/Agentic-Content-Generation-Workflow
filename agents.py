import google.generativeai as genai
from config import Config

genai.configure(api_key=Config().gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def ai_writer_spin_chapter(original_text: str) -> str:
    prompt = f"""
    You are an AI Writing Assistant tasked with modernizing classic literature.
    Your goal is to rewrite the following chapter in a more contemporary, engaging, and slightly more descriptive style.
    Preserve all key plot points, character interactions, and the overall atmosphere. Do not add new plot elements.

    Here is the original chapter to rewrite:
    ---
    {original_text}
    ---
    Please provide only the rewritten chapter text as your response.
    """

    try:
        print("Sending text to AI Writer...")
        response = model.generate_content(prompt)
        print("AI Writer finished.")
        return response.text
    except Exception as e:
        print(f"An error occurred with the AI Writer: {e}")
        return "--- AI WRITER FAILED ---"

def ai_reviewer_critique(original_text: str, spun_text: str) -> str:
    """
    Takes the original and spun text, and uses an LLM to provide a critique.
    """
    prompt = f"""
    You are an AI Quality Assurance Editor. Your task is to review a rewritten chapter against the original.
    Analyze the following two versions of a chapter.

    Your review should be concise and structured in three parts:
    1.  **Overall Match:** A single sentence stating how well the rewritten version matches the tone and plot of the original.
    2.  **Key Improvement:** Point out one specific thing the writer did well (e.g., "The description of the landscape was more vivid").
    3.  **Suggestion for Change:** Suggest one specific improvement (e.g., "The dialogue for character X could be more impactful").

    **Original Chapter:**
    ---
    {original_text}
    ---

    **Rewritten Chapter:**
    ---
    {spun_text}
    ---
    Please provide only the structured review as your response.
    """

    try:
        print("Sending texts to AI Reviewer...")
        response = model.generate_content(prompt)
        print("AI Reviewer finished.")
        return response.text
    except Exception as e:
        print(f"An error occurred with the AI Reviewer: {e}")
        return "--- AI REVIEWER FAILED ---"


def ai_writer_spin_with_feedback(previous_draft: str, combined_human_feedback: str) -> str:
    """
    Takes a previous draft and human feedback to create a refined version.
    """
    prompt = f"""
    You are an AI Writing Assistant. Your previous draft of a chapter has been reviewed by a human editor.
    Your task is to rewrite the draft, carefully incorporating all of the following feedback.

    **Previous Draft to be revised:**
    ---
    {previous_draft}
    ---

    **Human Editor's Instructions for this revision:**
    ---
    {combined_human_feedback}
    ---

    Please provide only the new, fully refined chapter text as your response.
    """
    try:
        print("Re-spinning chapter with human feedback...")
        response = model.generate_content(prompt)
        print("Refinement complete.")
        return response.text
    except Exception as e:
        print(f"An error occurred with the AI Writer during refinement: {e}")
        return "--- AI WRITER FAILED ON REFINEMENT ---"
    
