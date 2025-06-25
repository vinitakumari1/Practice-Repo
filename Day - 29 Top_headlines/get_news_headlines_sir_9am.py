# Steps - 
# Identify Import
# Load GPT2Tokenizer and GPT2Model
# Get the news article (article)
# Get the Poosible Headlines (Candidate)
# Get Tokens for news article (article)
#   Convert to Tensor and send to Model 
#   Get the Full Embeddings for news article (article)
#   Get the Mean Embeddings for news article (article) from Full Embeddings
# Get the Poosible Headlines (Candidate) - Repeat for all possible headlines
#   Convert to Tensor and send to Model 
#   Get the Full Embeddings for news article (article)
#   Get the Mean Embeddings for news article (article) from Full Embeddings
# Find Cosine of News (Mean Embeddings for news article ) with Candidates
#  Print Output Top  3 and Full List with Scores

from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

# Load the Model and Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

# Get the news Article 
article = """
OpenAI has released GPT-4o, a faster and more affordable language model that supports voice and vision.
It allows real-time reasoning across text, image, and audio, making it more interactive and accessible.
"""

# Get Possible Candidates
headlines = [
    "OpenAI launches GPT-4o with multimodal support",
    "NASA prepares new moon mission for 2026",
    "Stocks rise after major tech earnings",
    "GPT-4o enables live voice and image input",
    "AI model from OpenAI can now talk and see",
    "New earthquake detected in the Pacific region"
]

#Get mean embeddings for the article
def get_mean_embeddings (input_text):
    # Get the Tokens from the input_text
    model_input = tokenizer(input_text, return_tensors="pt")

    # Load Model with minimum features, for embeddings only
    with torch.no_grad():
        model_output = model (**model_input)
        mean_embeddings = model_output.last_hidden_state.mean(dim=1) # [1, 768]
    return mean_embeddings

article_embeddings = get_mean_embeddings(article) # will be later Saved to Vector DB


#get embeddings for headlines 
results = []
for headline in headlines:
    headline_embeddings = get_mean_embeddings(headline) # Save to Vector DB
    # get score between article embedding and headline embedding
    score = F.cosine_similarity(article_embeddings,headline_embeddings ).item()
    results.append((headline,score ))

#to get top 3 headlines based on score
results.sort(key= lambda x: x[1],reverse=True)
print ("Top 3 Similar headlines are: \n")


for i in range(3):
    headline, score = results[i]
    print  (f"{i + 1} - {headline} - Score {score:.4f}")

for headline, score in results:
    print (f"{score} -> {headline}")