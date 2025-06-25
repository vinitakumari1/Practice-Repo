import json
import requests
import logging 

logging.basicConfig(
    filename= 'newsapilog.log',
    level= logging.INFO,
    format= '%(asctime)s - %(lineno)d - %(levelname)s -  %(message)s'
)

URL='https://newsapi.org/v2/everything'
API="30ddaecf408f424bbb54466657be12fb"

def fetch_news(API,pageSize,query):
   
    response = requests.get(URL, params=
        {
        "apiKey" : API,
        "pageSize" : pageSize,
        "q" : query,
        
        }
    )
    logging.info("fetched news successfully")
    output = response.json()
    return output
    

if __name__== "__main__":
    try:
        news= fetch_news(API,5,query="bitcoin")
        with open("f.json","w",encoding="utf-8") as f:
            json.dump(news,f,indent=4)
        logging.info("printing news")
        print(f"fetched {len(news.get("articles"))} articles")
        
    except Exception as e:
        logging.info(str(e))

