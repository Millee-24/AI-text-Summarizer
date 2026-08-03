import re
import html

def clean_text(text):
    #Replacing the unicode characters, so that summary can include it because regex will ignore these as they are not included in the rules
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u201C', '"')
    text = text.replace('\u201D', '"')
    text = text.replace('\u2013', '-')
    text = text.replace('\u2014', '-')
    text = text.replace('\u2026', '...')
    #Some of the websites also contain html enities like &lt (<) and &gt (>) so instead of removing them because some of them can be essential and can lead to loss of meaning if removed
    text = html.unescape(text)
    #We are removing any leftover plain text urls
    #It will remove any text starting with http and www 
    text = re.sub(r"http\S+|www\S+", " ", text)
    #We are removing citations like [1], [2]
    text = re.sub(r"\[\d+\]"," ", text)
    #We are removing any white spaces
    text = re.sub(r"\s+"," ", text).strip()
    #We are removing special characters (here ^ not these characters) except what is mentioned in the sqaure bracket everyhting else will be replaced with empty space
    text = re.sub(r"[^a-zA-Z0-9\?\.\!\s\,\%\$\;\:\(\)\'\-]", " ", text)
    # Final whitespace cleanup
    text = re.sub(r"\s+", " ", text).strip()

    return text

if __name__ == "__main__":
    sample_text = """Climate change is one of the most serious 
    threats facing humanity today. Scientists have warned that 
    global temperatures are rising at an unprecedented rate [1]. 
    The main cause is greenhouse gas emissions from burning 
    fossil fuels. Read more at https://example.com/climate. 
    Economic costs could reach $100 billion by 2050."""

    cleaned = clean_text(sample_text)
    print("CLEANED TEXT:")
    print(cleaned)


    
