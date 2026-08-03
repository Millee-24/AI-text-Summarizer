from deep_translator import GoogleTranslator

def summary_translation(persona_summary, target=None):
    translated = GoogleTranslator(
        source="auto",
        target=target).translate(persona_summary)
    return translated 


if __name__ == "__main__":
    from scraper import get_text
    from preprocess import clean_text
    from summarizer import summarize_text
    from persona import rewrite_the_summary_for_persona

    url = "https://en.wikipedia.org/wiki/Gold"
    text = get_text("url", url=url)
    cleaned_text = clean_text(text)
    summary, stats = summarize_text(cleaned_text)
    persona_summary = rewrite_the_summary_for_persona(summary=summary, persona="Researcher")
    translated_summary = summary_translation(persona_summary=persona_summary, target="pa")
    print(translated_summary)

