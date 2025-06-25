import json
import requests
import logging 
import torch
import torch.functional as F
import GPT2Tokenizer,GPT2LMHeadModel,GPT2Model

logging.basicConfig(
    filename= 'newsapilog.log',
    level= logging.INFO,
    format= '%(asctime)s - %(lineno)d - %(levelname)s -  %(message)s'
)

URL='https://newsapi.org/v2/everything'
API="30ddaecf408f424bbb54466657be12fb"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
emb_model = GPT2Model.from_pretrained("gpt2")
gen_model = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizer.pad_token = tokenizer.eos_token
gen_model.pad_token_id = gen_model.config.eos_token_id
emb_model.pad_token_id = emb_model.config.eos_token_id


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
    
def get_mean_embeddings(input_text):
    tokens=tokenizer.tokens(input_text,return_tensors="pt")
    with torch.no_grad(tokens):
        outputs=emb_model(**tokens)
    return outputs.last_hidden_state.mean(dim=1)


def generate_headlines(prompt):
    prompt_tokens=tokenizer(prompt,return_tensors="pt")
    headlines=gen_model.generate(
        prompt_tokens,
        num_return_sequences=3
        do_sample=True
        temperature=0.8,
        max_new_tokens=50,
        top_k = 50,
        top_p = 0.95

    )

    return [tokenizer.decode(headline, skip_special_tokens=True).replace(prompt, "").strip() for headline in headlines]















if __name__== "__main__":
    try:
        news= fetch_news(API,5,query="bitcoin")
        with open("f.json","w",encoding="utf-8") as f:
            json.dump(news,f,indent=4)
        logging.info("printing news")
        print(f"fetched {len(news.get("articles"))} articles")
        
    except Exception as e:
        logging.info(str(e))

