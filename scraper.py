import requests
from bs4 import BeautifulSoup 
#Here, we are scraping the text from the given url and removing all the unwanted tags like the:
#script, nav, header, footer, img, picture, video and audio tags. We collecting all the paragraphs from the paragrph tag and joining them toegther to get the complete text. 

def scrape_text_from_url(url):
    try:
        #We using header because some websites may block requests that do not have a user-agent header, which can make it look like th request came from a bot. (It refers to the http request headers)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers,timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style","header","footer","nav","img","picture","video","audio"]):
                tag.decompose()
            
            paragraphs = soup.find_all("p")
            #content_tags = soup.find_all(["p", "li"])

            # Filter short paragraphs
            #filtered = [
                #tag.get_text().strip() for tag in content_tags
                #if len(tag.get_text().strip()) > 30
            #]
            #filtered_paragraphs = [para.get_text() for para in paragraphs
                                   #if len(para.get_text().strip()) > 30]
            #text = " ".join(filtered)
            text = " ".join(para.get_text() for para in paragraphs)
            return text 
            #if not text.strip():
                #print("Warning: No text found.")
                #return None

            #return text
        elif response.status_code == 403:
            print("Access denied, the website may have restrictions on web scarping. Try using a different url")
        elif response.status_code == 404:
            print("The requested page was not found")
        else:
            print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

    
def get_text(text_type, text = None, url = None):
    if text_type == "url":
        if url:
            return scrape_text_from_url(url)
        else:
            print("URL is required for text type 'url'")
            return None
    elif text_type == "text":
        if text:
            return text
        else:
            print("Text is required for text type 'text'")
            return None
    else:
        print("Invalid text type. Please choose 'url' or 'text'.")
        return None

if __name__ == "__main__":
    from preprocess import clean_text
    url = "https://my.clevelandclinic.org/health/symptoms/21660-inflammation"
    text = get_text("url", url=url)
    print(text[:3000])
    total_char = len(text)
    print(f"Total characters scraped: {total_char}")
    print("Cleaned Text: ")
    cleaned_text = clean_text(text)
    print(cleaned_text[:3000])

