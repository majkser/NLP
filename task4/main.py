from BasicTokenizer import BasicTokenizer
from RegexTokenizer import RegexTokenizer
from GPT4Tokenizer import GPT4Tokenizer
import tiktoken

if __name__ == "__main__":
    f = open("train.txt", "r", encoding="utf-8")
    text = f.read()
    f.close()
    text = text.replace("\n", " ")
    
    test = "Hello, world! I'm testing the RegexTokenizer."
    
    basic_tokenizer = BasicTokenizer()
    basic_tokenizer.train(text, vocab_size=286, verbose=True)
    encoded_basic = basic_tokenizer.encode(test)
    print("Basic tokenizer Decoded == original: ", basic_tokenizer.decode(encoded_basic) == test)
    
    regex_tokenizer = RegexTokenizer()
    regex_tokenizer.train(text, vocab_size=286, verbose=True)
    
    encoded = regex_tokenizer.encode(test)
    print("Regex tokenizer Decoded == original: ", regex_tokenizer.decode(encoded) == test)
    
    enc = tiktoken.get_encoding("cl100k_base") # this is the GPT-4 tokenizer
    gpt4_test = 'hello world!!!? (안녕하세요!) lol123 😉'
    print("tiktoken GPT-4 Decoded == original: ", enc.decode(enc.encode(gpt4_test)) == gpt4_test)
    print('tiktoken encoded == regex_tokenizer encoded: ', enc.encode(gpt4_test) == regex_tokenizer.encode(gpt4_test))
    
    gpt4_tokenizer = GPT4Tokenizer()
    print("GPT4Tokenizer Decoded == original: ", gpt4_tokenizer.decode(gpt4_tokenizer.encode(gpt4_test)) == gpt4_test)
    print("GPT4Tokenizer encoded == tiktoken GPT-4 encoded: ", gpt4_tokenizer.encode(gpt4_test) == enc.encode(gpt4_test))
    
    f2 = open("taylorswift.txt", "r", encoding="utf-8")
    taylorswift_text = f2.read()
    f2.close()
    
    print('Taylor Swift encode comparison - GPT4Tokenizer encoded == tiktoken GPT-4 encoded: ', gpt4_tokenizer.encode(taylorswift_text) == enc.encode(taylorswift_text))