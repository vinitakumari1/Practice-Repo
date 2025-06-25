from transformers import GPT2Tokenizer, GPT2Model
import torch
import torch.nn.functional as F

# Step 1: Load article (single text block)
with open("article.txt", "r", encoding="utf-8") as a:
    article_text = a.read().strip()

# Step 2: Load headlines (list of lines)
with open("headlines.txt", "r", encoding="utf-8") as h:
    headlines_list = [line.strip() for line in h if line.strip()]  # Remove blank lines too

# Step 3: Load tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2Model.from_pretrained("gpt2")

# Step 4: Function to get mean embeddings
def get_mean_embeddings(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        mean_embeddings = outputs.last_hidden_state.mean(dim=1)
    return mean_embeddings

# Step 5: Compute embeddings
article_embedding = get_mean_embeddings(article_text)

results = []
for headline in headlines_list:
    headline_embedding = get_mean_embeddings(headline)
    score = F.cosine_similarity(article_embedding, headline_embedding).item()
    results.append((headline, score))

# Step 6: Sort and print top 4
results.sort(key=lambda x: x[1], reverse=True)

print("Top 4 Similar Headlines:\n")
for i, (headline, score) in enumerate(results[:4], 1):
    print(f"{i} - {headline} - Score {score:.4f}")


print("----------------------------------------------------------------")

print("All Headlines with Decreasing Scores:\n")
for headline, score in results:
    print(f"{score:.4f} -> {headline}")