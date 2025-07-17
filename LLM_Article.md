**Masterclass: GPT-2/4 — Tokens, Embeddings, Vector Search, FAISS, MongoDB & FastAPI
Welcome to the ultimate guide to building LLM applications using**

1. GPT-2/GPT-4

2. Embeddings & Vector Search

3. MongoDB

4. FastAPI

# Whether you're building a resume QnA bot, a chatbot, or a semantic search engine, this masterclass connects the dots from theory to implementation.

**Table of Contents**

1. Understanding Tokens in GPT

2. Embeddings: The Brain of Semantic Search

3. Vector Search using FAISS

4. Storing Resume Metadata in MongoDB

5. Exposing LLM APIs using FastAPI

6. End-to-End Architecture

7. Example Project: Resume QnA System

8. Conclusion: How it all connects


**1. Understanding tokens in GPT**

    Tokens are the smallest meaningful units of text that an AI model works with.It can be a word, a part of a word (like a subword or syllable), or even a single character. Tokenization, the process of converting text into these units, is crucial for enabling AI to understand, analyze, and generate human language. 

    In the context of GPT models (like GPT-2 and GPT-4), a token is a unit of text that the model processes. Tokens can be:

    Whole words (e.g., hello)

    Parts of words (e.g., un, believ, able)

    Punctuation marks (e.g., ., ,, !)

    Even white space ( )

    Why Tokens Matter ?
    Tokens directly affect:

    1. Input limits: GPT-2 only supports up to 1024 tokens; GPT-4 supports up to 32,768 tokens (Turbo).

    2. Cost: OpenAI charges based on tokens — both input and output.

    3. Performance: More tokens = more compute time.

**2. Embeddings : The brain of Semantic Search**

    Embeddings are numerical representations of text capturing meaning.

   ```python
    from openai import OpenAI
    openai.embeddings.create(model="text-embedding-3-small", input="What is FastAPI?")
   ```








