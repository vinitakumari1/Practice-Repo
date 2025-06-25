import requests
import logging 



NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "30ddaecf408f424bbb54466657be12fb"
HEADLINE_COUNT =3  
ARTICLE_COUNT = 5

#logging.basicConfig(level=logging.INFO, format= "%(asctime)s - %(levelname)s -%(message)s") -> sir 


logging.basicConfig(
    filename='news_article.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)



def fetch_news_articles(api_key, count) -> list[dict]:
    logging.info ("Fetching new articles.... Please wait")
    news_api_response =  requests.get(NEWS_API_URL, params = {
        "apiKey" : api_key,
        "country" : "us",
        "pageSize" : count
    })

    news_api_response.raise_for_status()
    news_articles = news_api_response.json().get("articles", [])
    logging.info (f"Fetched {len(news_articles)} articles")
    return news_articles



if __name__ == "__main__":
    try:
        articles = fetch_news_articles(API_KEY, ARTICLE_COUNT) # Get top 5 Articles
        print (articles)
    except Exception as e:
        logging.info (str(e))
    