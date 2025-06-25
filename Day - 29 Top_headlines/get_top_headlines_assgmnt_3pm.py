from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F


#Load the model and the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model= GPT2Model.from_pretrained("gpt2")

#Get the news article

article ="""

The United States and India recently announced a rollback of certain tariffs 
imposed during previous trade disputes. The move is expected to boost bilateral trade, 
particularly in sectors like agriculture, electronics, and manufacturing. 
Economists believe this step will enhance market access and reduce costs for exporters on both sides,
 while signaling improved geopolitical alignment between the two democracies.

"""

#Get the possible headlines

headlines = [

"US and India remove tariffs to boost trade ties",
"India launches lunar probe to explore moon's south pole",
"Tariff rollback improves US-India manufacturing access",
"Stock markets dip amid inflation concerns in Asia",
"Improved trade relations could strengthen US-India alliance",
"India bans certain Chinese tech products from ports"

]

#Get mean embeddings for the article
def get_mean_embeddings(input_text):
    input_model=tokenizer(input_text,return_tensors="pt")
    with torch.no_grad():
        output_model=model(**input_model)
        mean_embeddings=output_model.last_hidden_state.mean(dim=1)
    return mean_embeddings

article_embeddings = get_mean_embeddings(article)

results = []
for headline in headlines:
    headline_embeddings = get_mean_embeddings(headline) 
    score = F.cosine_similarity(article_embeddings,headline_embeddings).item()
    results.append((headline,score ))

#to get top 4 headlines based on score
results.sort(key= lambda x: x[1],reverse=True)
print ("Top 4 Similar headlines are: \n")


for i in range(4):
    headline, score = results[i]
    print  (f"{i + 1} - {headline} - Score {score:.4f}")

for headline, score in results:
    print (f"{score} -> {headline}")



