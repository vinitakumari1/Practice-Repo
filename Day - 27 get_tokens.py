from transformers import GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


input_string = input("please enter a text string")

tokens = tokenizer.tokenize(input_string) #gives tokens in list format

print(tokens)




