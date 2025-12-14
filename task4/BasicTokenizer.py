class BysicTokenizer: 
    def train(self, text, vocab_size, verbose=False):
        tokens = text.encode('utf-8')
        tokens = list(map(int, tokens))
        print(len(text))
        #print(tokens)
        print(len(tokens))
        
        count = self.__get_pair_counts(tokens)
        max_count = max(count, key=count.get)
        print((max_count))
        
        print(len(self.__merge_pair(tokens, max_count, 69)))
            
    
    def encode(self, text):
        pass
    
    def decode(self, ids):
        pass

    def __get_pair_counts(self, tokens: list[int]) -> dict:
        count = {}
        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i + 1])
            if pair in count:
                count[pair] += 1
            else:
                count[pair] = 1
        return count
    
    def __merge_pair(self, tokens: list[int], pair: tuple[int, int], id: int) -> list[int]:
        merged_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
                merged_tokens.append(id)
                i += 2
            else:
                merged_tokens.append(tokens[i])
                i += 1
        return merged_tokens
    
if __name__ == "__main__":
    tokenizer = BysicTokenizer()
    
    # prepare training data(text)
    f = open("train.txt", "r", encoding="utf-8")
    text = f.read()
    f.close()
    text = text.replace("\n", " ")
    
    tokenizer.train(text, vocab_size=100, verbose=True)
    encoded = tokenizer.encode("This is a sample text.")
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)