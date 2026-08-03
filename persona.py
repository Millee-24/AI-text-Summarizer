import os 
from google import genai
Client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#Here we are intilializing that whenever interact with gemini use this api key, it is like your authorization 

persona_prompts = {
    "Child":
    """ 
    Rewrite the following summary for a child.
    Write chemical formulas in plain text like Au(CN)2- not $[\\text{{Au}}(\\text{{CN}})_2]^-$.
    Do not use any markdown formatting like **, ##.
    Keep it under {word_limit} words 
    Use:
    -simple words
    -avoid technical jargon
    -short sentences 
    -simple explanations 
    -friendly tone

"""
,
  "Student":
  """ 
  Do not use LaTeX or markdown formatting.
  Write chemical formulas in plain text like Au(CN)2- not $[\\text{{Au}}(\\text{{CN}})_2]^-$.
  Do not use any markdown formatting like **, ##.
  Keep it under {word_limit} words 
  Rewrite the following summary for a student.
  Use:
  -relevant points from exam point of view 
  -important concepts 
  -clarity of concept 
  -concise explanation
"""
,
   "Teacher":
   """
   Rewrite the following summary for a teacher.
   Write chemical formulas in plain text like Au(CN)2- not $[\\text{{Au}}(\\text{{CN}})_2]^-$.
   Do not use any markdown formatting like **, ##.
   Keep it under {word_limit} words  
   -educational tone 
   -structural informations 
   -clear explanations 

   """
,
  "Researcher":
  """
  Rewrite the following summary for a reasearcher 
  Write chemical formulas in plain text like Au(CN)2- not $[\\text{{Au}}(\\text{{CN}})_2]^-$.
  Do not use any markdown formatting like **, ##.
  Keep it under {word_limit} words 
  -technical terminology
  -formal languages 
  -detailed explanations 
  -precise wording """
}

def rewrite_the_summary_for_persona(summary, persona=None, word_limit=None):
    if persona is None:
        persona = "Student"
    persona = persona.title()

    if word_limit is None:
        word_limit = len(summary.split())
        
    if persona in persona_prompts:
        prompt = persona_prompts[persona].format(word_limit=word_limit)
        final_prompt = f"{prompt}\n        SUMMARY:{summary}"
        
        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = Client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=final_prompt
                )
                return response.text.strip()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2) # wait 2 seconds before retrying
                
    else:
        return "Persona not supported"
    


def calculate_persona_stats(original_summary, persona_summary):
        lexrank_words = len(original_summary.split())
        persona_words = len(persona_summary.split())
        words_reduced = lexrank_words - persona_words
        compression = round((1 - persona_words / lexrank_words) * 100) if lexrank_words > 0 else 0

        return {
            "lexrank_words": lexrank_words,
            "persona_words": persona_words,
            "words_reduced": words_reduced,
            "compression": compression
        }
    
if __name__ == "__main__":
    from scraper import get_text
    from preprocess import clean_text
    from summarizer import summarize_text

    url = "https://en.wikipedia.org/wiki/Gold"
    text = get_text("url", url=url)
    cleaned_text = clean_text(text)
    summary,stats = summarize_text(cleaned_text)
    word_limit = stats['Summary_words']



    #sample_summary = """
    #Bitcoin is a decentralized digital currency
    #that works without banks using blockchain technology.
    #"""
    persona_summary = rewrite_the_summary_for_persona(summary=summary, persona="Student", word_limit=word_limit)
    print("PERSONA SUMMARY")
    print(persona_summary)
    persona_stats = calculate_persona_stats(original_summary=summary, persona_summary=persona_summary)
    print("---")
    print(f"LexRank words  : {persona_stats['lexrank_words']}")
    print(f"Persona words  : {persona_stats['persona_words']}")
    print(f"Words reduced  : {persona_stats['words_reduced']}")
    print(f"Compression    : {persona_stats['compression']}%")




    
