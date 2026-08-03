import re
import yake 
from wordcloud import WordCloud
import matplotlib.pyplot as plt 


def extract_keywords(text, num_keywords=10):
    #Initializing the yake extracter 
    keyword_extracter = yake.KeywordExtractor(
        lan = "en", #langauge
        n=3, #maximum words that will be displayed per keyword
        dedupLim=0.8, #removes dupliacte similar keywords 
        top=num_keywords*7) #number of keywords to return 
    #Extracting keywords from the text
    #Yake returns a list of tuples (keyword, score)
    keywords_with_scores = keyword_extracter.extract_keywords(text)
    seen_words = set()
    filtered = []
    #filtered = [(kw, score) for kw, score in keywords_with_scores
                #if len(kw.split()) >= 2]
    for kw, score in keywords_with_scores:
        words = kw.lower().split()

        # Skip single word keywords
        if len(words) < 2:
            continue

        # Skip if majority of words already seen in previous keywords
        overlap = sum(1 for w in words if w in seen_words)
        if overlap >= len(words) - 1:
            continue

        # Add words to seen set
        seen_words.update(words)
        filtered.append((kw, score))
    

    #Seperating out the keywords and scores 

    ranked_keywords = [kw for kw, score in filtered]
    ranked_with_scores = [(score,kw) for kw, score in filtered]
    return ranked_keywords[:num_keywords], ranked_with_scores[:num_keywords]

def generate_wordcloud(ranked_keywords):
    text = ' '.join(ranked_keywords)
    wc = WordCloud(width=800, height=400, background_color='white')
    wordcloud = wc.generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

def highlight_keywords(summary, ranked_keywords):
    highlighted_summary = summary
    for keywords in ranked_keywords:
        highlighted_summary = re.sub(re.escape(keywords), lambda match: f'<mark style="background-color:#FFE066; padding:2px 4px; border-radius:3px">{match.group()}</mark>', highlighted_summary, flags = re.IGNORECASE)
    return highlighted_summary

if __name__ == "__main__":
    from scraper import get_text
    from preprocess import clean_text

    #text = """Natural language processing (NLP) is a subfield of artificial intelligence
     # (AI) that focuses on the interaction between computers and humans through 
      #natural language. The ultimate goal of NLP is to enable computers to 
      #understand, interpret, and generate human language in a valuable way.
      #NLP combines computational linguistics with machine learning, deep learning,
      #statistical modeling, and more. It has applications in various domains such 
      #as chatbots, sentiment analysis, language translation, and information 
      #retrieval."""
    url = "https://en.wikipedia.org/wiki/Gold"  

    #text = get_text("text", text=text)
    text = get_text("url", url=url)
    #cleaned_text = clean_text(text)
    cleaned_text = clean_text(text)

    ranked_keywords, ranked_with_scores = extract_keywords(cleaned_text)
    highlight = highlight_keywords(cleaned_text, ranked_keywords)
    print("Top Keywords:")
    for i, (score, phrase) in enumerate(ranked_with_scores, 1):
        print(f"{i}. {phrase} (score: {score})")

    print("---")
    generate_wordcloud(ranked_keywords)



    
    
