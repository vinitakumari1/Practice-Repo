import requests
import logging 
import json
import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Model

NEWS_API_URL = "https://newsapi.org/v2/everything"
API_KEY = "30ddaecf408f424bbb54466657be12fb"
ARTICLE_COUNT = 5

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id

logging.basicConfig(
    filename='Day-32-news_article_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_news_articles(api_key, count, query) -> dict:
    logging.info(f"Fetching news from NewsAPI for query: {query}")
    response = requests.get(NEWS_API_URL, params={
        "apiKey": api_key,
        "q": query,
        "pageSize": count
    })
    response.raise_for_status()
    return response.json()

def get_mean_embedding(input_text):
    input_text_tokens = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        embeddings = emb_model(**input_text_tokens)
    return embeddings.last_hidden_state.mean(dim=1)

def generate_headlines(prompt):
    news_headline_tokens = tokenizer(prompt, return_tensors="pt").input_ids
    headlines = gen_model.generate(
        news_headline_tokens,
        do_sample=True,
        num_return_sequences=3,
        max_new_tokens=50,
        temperature=0.8,
        top_k=50,
        top_p=0.95
    )
    return [tokenizer.decode(headline, skip_special_tokens=True).replace(prompt, "").strip() for headline in headlines]


# Parameter	Meaning (Simple Explanation)
# news_headline_tokens :	This is your input prompt, converted into tokens (e.g., "Breaking News: ").
# do_sample=True : Instead of always choosing the "most likely next word", it randomly samples from top options.
# num_return_sequences=3 : You want 3 different versions (headlines) to be generated.
# max_new_tokens=50	: Each headline can be up to 50 tokens (words) long.
# temperature=0.8 : Controls randomness. Lower = safer/more predictable. Higher = more creative.
# top_k=50 : Only consider the top 50 most likely words when picking the next one.
# top_p=0.95 : Use only the smallest group of top words that make up 95% probability.


def process_and_embed_headlines(news_response):
    articles = news_response.get("articles", [])

    for article in articles:
        title = article.get("title") or ""
        description = article.get("description") or ""
        content = article.get("content") or ""

        news_text = f"{title}. {description}. {content}".strip()
        if not news_text:
            article["headlines"] = []
            continue

        prompt = f"Generate a headline for this news:\n{news_text}\nHeadline:"
        headline_candidates = generate_headlines(prompt)

        #FOR SCORES
        news_text_embedding = get_mean_embedding(prompt)

        result = []
        for headline in headline_candidates:
            headline_mean_embedding = get_mean_embedding(headline)
            score = F.cosine_similarity(headline_mean_embedding, news_text_embedding).item()
            result.append({
                "headline": headline,
                "score": round(score, 4)
            })

        article["headlines"] = result
    logging.info("Processed the news with headlines embedded")
    return news_response

if __name__ == "__main__":
    try:
        query = "bitcoin"
        news_data = fetch_news_articles(API_KEY, ARTICLE_COUNT, query)

        # Embed generated headlines into each article
        full_news_data = process_and_embed_headlines(news_data)

        # Save the enriched news data
        with open("Embedded_headlines_with_news.json", "w", encoding="utf-8") as f:
            json.dump(full_news_data, f, indent=2)

        print("\n Headlines embedded and saved in 'full_response.json'.")

    except Exception as e:
        logging.exception("Error occurred.")
