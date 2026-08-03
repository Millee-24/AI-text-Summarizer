from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
language = "english"

def count_sentences(text):
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    return len(list(parser.document.sentences))

def count_words(text):
    return len(text.split())

def summarize_text(text):
    total_sentences = count_sentences(text)
    total_words = count_words(text)
    #Through this we are ensuring that the summary does not exceed 20% of the original text.
    summary_length = max(1, round(total_sentences * 0.2))
    parser = PlaintextParser.from_string(text, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = LexRankSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    summary = summarizer(parser.document, summary_length)
    summary =  " ".join(str(sentence) for sentence in summary)
    summary_words = count_words(summary)
    summary_sentences_count = count_sentences(summary)
    stats = {
        "Original_sentences":total_sentences, "Summary_sentences":summary_sentences_count, "Original_words":total_words,
        "Summary_words":summary_words,"words_reduced":total_words - summary_words, "compression":  round((1 - summary_words / total_words) * 100)}
    return summary, stats


if __name__ == "__main__":
    from scraper import get_text
    from preprocess import clean_text
    from keywords import extract_keywords, highlight_keywords, generate_wordcloud


    url = "https://en.wikipedia.org/wiki/Gold"
    text = get_text("url", url=url)

    cleaned_text = clean_text(text)
    summary, stats = summarize_text(cleaned_text)

    print("SUMMARY:")
    print(summary)
    print("---")
    print(f"Original sentences : {stats['Original_sentences']}")
    print(f"Summary sentences  : {stats['Summary_sentences']}")
    print(f"Original words     : {stats['Original_words']}")
    print(f"Summary words      : {stats['Summary_words']}")
    print(f"Words reduced      : {stats['words_reduced']}")
    print(f"Compression        : {stats['compression']}%")
    print("---")

    ranked_keywords, ranked_with_scores = extract_keywords(cleaned_text)

    print("Top Keywords:")
    for i, (score, phrase) in enumerate(ranked_with_scores, 1):
        print(f"{i}. {phrase} (score: {score})")

    print("---")

    highlighted_summary = highlight_keywords(summary, ranked_keywords)

    with open("test.html", "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <body style="font-family:Arial; padding:30px; font-size:16px; 
                     max-width:800px; line-height:1.8">
        <h2>Summary</h2>
        <p>{highlighted_summary}</p>
        <hr>
        <h3>Keywords</h3>
        <p>{', '.join(ranked_keywords)}</p>
        <hr>
        <h3>Stats</h3>
        <p>Original sentences: {stats['Original_sentences']}</p>
        <p>Summary sentences: {stats['Summary_sentences']}</p>
        <p>Original words: {stats['Original_words']}</p>
        <p>Summary words: {stats['Summary_words']}</p>
        <p>Words reduced: {stats['words_reduced']}</p>
        <p>Compression: {stats['compression']}%</p>
        </body>
        </html>
        """)

    print("Open test.html in your browser to see yellow highlighting")
    #We are generating wordcloud 
    generate_wordcloud(ranked_keywords)
   









