from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import nltk

# Download required NLTK data for sumy tokenizers
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

from scraper import get_text
from preprocess import clean_text
from summarizer import summarize_text
from keywords import extract_keywords, highlight_keywords
from persona import rewrite_the_summary_for_persona, calculate_persona_stats
from translate import summary_translation, translate_keywords

app = Flask(__name__)
CORS(app)

LANGUAGES = {
    "Hindi": "hi", "Punjabi": "pa", "French": "fr",
    "Spanish": "es", "German": "de", "Arabic": "ar",
    "Chinese (Simplified)": "zh-CN", "Tamil": "ta",
    "Telugu": "te", "Bengali": "bn", "Japanese": "ja",
    "Korean": "ko", "Portuguese": "pt", "Russian": "ru",
    "Italian": "it", "Turkish": "tr", "Urdu": "ur",
    "Marathi": "mr", "Gujarati": "gu", "Kannada": "kn",
}

@app.route('/api/summarize', methods=['POST'])
def summarize_api():
    try:
        data = request.json
        input_type = data.get('type') # 'text' or 'url'
        input_content = data.get('content')
        persona = data.get('persona', 'Researcher')
        language = data.get('language', 'None')

        raw_text = None
        if input_type == 'url':
            raw_text = get_text("url", url=input_content)
            if not raw_text:
                return jsonify({"error": "Could not extract text from the given URL."}), 400
        elif input_type == 'text':
            raw_text = input_content
            if not raw_text or not raw_text.strip():
                return jsonify({"error": "No text provided."}), 400
        else:
            return jsonify({"error": "Invalid input type. Must be 'text' or 'url'."}), 400

        # Step 1: Clean text
        cleaned = clean_text(raw_text)
        if not cleaned:
            return jsonify({"error": "Text is empty after cleaning."}), 400

        # Step 2: Summarize
        summary, stats = summarize_text(cleaned)
        word_limit = stats["Summary_words"]

        # Step 3: Keywords
        ranked_kw, ranked_scores = extract_keywords(cleaned)

        # Step 4: Persona Adaptation
        persona_summary = rewrite_the_summary_for_persona(
            summary=summary, persona=persona, word_limit=word_limit
        )
        persona_stats = calculate_persona_stats(summary, persona_summary)

        # Step 5: Highlight keywords in summary
        highlighted = highlight_keywords(persona_summary, ranked_kw)

        # Step 6: Translation
        translated_text = None
        display_kw = ranked_kw

        if language != "None" and language in LANGUAGES:
            lang_code = LANGUAGES[language]
            translated_text = summary_translation(
                persona_summary=persona_summary,
                target=lang_code
            )
            display_kw = translate_keywords(ranked_kw, target=lang_code)

        total_comp = round(
            (1 - persona_stats["persona_words"] / stats["Original_words"]) * 100
        ) if stats["Original_words"] > 0 else 0

        return jsonify({
            "success": True,
            "original_words": stats["Original_words"],
            "lexrank_words": stats["Summary_words"],
            "persona_words": persona_stats["persona_words"],
            "words_removed": stats["Original_words"] - persona_stats["persona_words"],
            "compression": f"{total_comp}",
            "highlighted_summary": highlighted,
            "raw_summary": persona_summary,
            "translated_summary": translated_text,
            "keywords": display_kw
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
