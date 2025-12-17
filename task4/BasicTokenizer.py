class BasicTokenizer:
    def __init__(self):
        self.merges = {}
    
    def train(self, text: str, vocab_size: int, verbose=False):
        self.merges = {} # reset merges on each training
        self.vocab = {i: bytes([i]) for i in range(256)} # initialize vocab (first 256 tokens without merges)
        tokens = text.encode('utf-8')
        tokens = list(map(int, tokens))
        
        if verbose:
            print('length of the text: ', len(text))
            print('num of tokens: ', len(tokens))
            
        for i in range(vocab_size - 256):
            count  = self._get_pair_counts(tokens)
            if not count:
                break
            
            max_count = max(count, key=count.get)
            tokens = self._merge_pair(tokens, max_count, 256 + i)
            self.merges[max_count] = 256 + i # record the merge operation
            self.vocab[256 + i] = self.vocab[max_count[0]] + self.vocab[max_count[1]]
            if verbose:
                print(f"Merge pair: {max_count}, New token id: {256 + i}, New length: {len(tokens)}")
        
        if verbose:
            print('Training completed')
            print('Number of tokens after training: ', len(tokens))
            print('Compression ratio: ', f'{len(text) / len(tokens):.2f}')
        
    def encode(self, text) -> list[int]:
        tokens = list(text.encode('utf-8'))
        
        while len(tokens) > 1:
            pair_count = self._get_pair_counts(tokens)
            if not pair_count:
                break
            
            pair_with_smallest_id = ()
            for pair in pair_count:
                if pair in self.merges and self.merges[pair] < self.merges.get(pair_with_smallest_id, float('inf')):
                    pair_with_smallest_id = pair

            if pair_with_smallest_id == () or pair_with_smallest_id not in self.merges.keys():
                break
            
            tokens = self._merge_pair(tokens, pair_with_smallest_id, self.merges[pair_with_smallest_id])
                
        return tokens
            
    def decode(self, ids) -> str:
        for merge_pair, merge_id in self.merges.items():
            self.vocab[merge_id] = self.vocab[merge_pair[0]] + self.vocab[merge_pair[1]]
        
        return b''.join(self.vocab[id] for id in ids).decode('utf-8', errors='replace')

    def _get_pair_counts(self, tokens: list[int]) -> dict:
        count = {}
        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i + 1])
            if pair in count:
                count[pair] += 1
            else:
                count[pair] = 1
        return count
    
    def _merge_pair(self, tokens: list[int], pair: tuple[int, int], id: int) -> list[int]:
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
    tokenizer = BasicTokenizer()
    
    # prepare training data(text)
    f = open("train.txt", "r", encoding="utf-8")
    text = f.read()
    f.close()
    text = text.replace("\n", " ")
    
    new_vocab_size = 256 + 30
    
    tokenizer.train(text, vocab_size=new_vocab_size, verbose=True)
    encoded = tokenizer.encode("This is a sample text.")
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)