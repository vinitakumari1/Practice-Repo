import os
import requests
import json


API_URL = "https://newsapi.org/v2/everything"
API_KEY = "30ddaecf408f424bbb54466657be12fb"

SAVE_FOLDER="Query"

if os.path.exists(SAVE_FOLDER):
    
    for filename in os.listdir(SAVE_FOLDER):
        if filename.endswith(".json"):
            file_path = os.path.join(SAVE_FOLDER, filename)
            os.remove(file_path)


def download_news_article(url, params):
                
    if not os.path.exists(SAVE_FOLDER) :
        os.makedirs(SAVE_FOLDER,exist_ok=True)
    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json().get("articles", []) #This converts the HTTP response (which is in JSON format) into a Python dictionary.
        articles = articles[:pagesize]
        print(f"Fetched {len(articles)} articles.")
        return articles
    else:
        print("Failed to fetch articles:", response.status_code, str(response))
            
def save_news_article(articles):
    
    for i, article in enumerate(articles):
                filename = os.path.join(SAVE_FOLDER, f"article_{i+1}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(article, f, ensure_ascii=False, indent=2)
    print(f"Saved all articles in '{SAVE_FOLDER}' folder.")
       


if __name__ == "__main__":

    print("\nPlease Enter Input Paramaters :\n")
    q= input("Enter Query string : ")
    language = input("Enter Language : ")
    article_count=int(input("Enter No of Articles needed : "))
    pagesize=article_count
    params= {"q" : q,
             "language":language,
             "page_size":pagesize,
             "apiKey":API_KEY,
             "page":1
             }   

    articles= download_news_article(API_URL,params)
    
    save_news_article(articles)



