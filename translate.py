from deep_translator import GoogleTranslator

def summary_translation(persona_summary, target=None):
    if target is None:
        target = "hi"

    # Split into chunks of 4500 characters to stay under 5000 limit
    chunk_size = 4500
    chunks = [persona_summary[i:i+chunk_size] 
              for i in range(0, len(persona_summary), chunk_size)]

    translated_chunks = []
    for chunk in chunks:
        translated = GoogleTranslator(
            source="en",
            target=target
        ).translate(chunk)
        translated_chunks.append(translated)

    return " ".join(translated_chunks)


def translate_keywords(keywords, target=None):
    if target is None:
        target = "hi"
    
    translated_keywords = []
    for kw in keywords:
        translated = GoogleTranslator(source="en", target=target).translate(kw)
        translated_keywords.append(translated)
        
    return translated_keywords

if __name__ == "__main__":
    from scraper import get_text
    from preprocess import clean_text
    from summarizer import summarize_text
    from persona import rewrite_the_summary_for_persona

    url = "https://en.wikipedia.org/wiki/Gold"
    raw_text = get_text("url", url=url)
    cleaned_text = clean_text(raw_text)
    summary, stats = summarize_text(cleaned_text)
    persona_summary = rewrite_the_summary_for_persona(
        summary=summary, persona="Researcher"
    )

    print("PERSONA SUMMARY:")
    print(persona_summary)
    print("---")
    print(f"Persona summary length: {len(persona_summary)} characters")
    print("---")

    translated = summary_translation(persona_summary=persona_summary, target="hi")
    print("TRANSLATED:")
    print(translated)