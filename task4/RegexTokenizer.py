import regex as re
from BasicTokenizer import BasicTokenizer

GPT4_SPLIT_PATTERN = r"""'(?i:[sdmt]|ll|ve|re)|[^\r\n\p{L}\p{N}]?+\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]++[\r\n]*|\s*[\r\n]|\s+(?!\S)|\s+"""

class RegexTokenizer(BasicTokenizer):
    def __init__(self, pattern: str = GPT4_SPLIT_PATTERN):
            super().__init__()
            self.compiled_pattern = re.compile(pattern)
            self.merges = {}
            self.vocab = {i: bytes([i]) for i in range(256)} # initialize vocab (first 256 tokens without merges)

    def train(self, text: str, vocab_size: int, verbose: bool = False) -> None:
        text_chunks = self.compiled_pattern.findall(text)
        
        tokens = [list(chunk.encode('utf-8')) for chunk in text_chunks]
        
        if verbose:
            print('length of the text: ', len(text))
            print('num of tokens: ', sum(len(chunk) for chunk in tokens))
        
        for i in range(vocab_size - 256):
            count = {}
            for j in range(len(tokens)):
                chunk_count = self._get_pair_counts(tokens[j])
                for pair, cnt in chunk_count.items():
                    count[pair] = count.get(pair, 0) + cnt
            if not count:
                break
            
            max_count = max(count, key=count.get)
            tokens = [self._merge_pair(tokens[j], max_count, 256 + i) for j in range(len(tokens))]
            self.merges[max_count] = 256 + i # record the merge operation
            self.vocab[256 + i] = self.vocab[max_count[0]] + self.vocab[max_count[1]]
            if verbose:
                print(f"Merge pair: {max_count}, New token id: {256 + i}, New length: {sum(len(chunk) for chunk in tokens)}")
    
    def encode(self, text: str) -> list[int]:
        text_chunks = self.compiled_pattern.findall(text)
        tokens = []
        
        for chunk in text_chunks:
            chunk_tokens = super().encode(chunk)
            tokens.extend(chunk_tokens)

        return tokens

    # def decode(self, ids: list[int]) -> str:
    #     pass
    
if __name__ == "__main__":
    f = open("train.txt", "r", encoding="utf-8")
    text = f.read()
    f.close()
    text = text.replace("\n", " ")
    
    tokenizer = RegexTokenizer()
    tokenizer.train(text, vocab_size=286, verbose=True)
    encoded = tokenizer.encode("Hello, world! I'm testing the RegexTokenizer.")
    print("Encoded:", encoded)
    decoded = tokenizer.decode(encoded)
    print("Decoded:", decoded)
    print(decoded == "Hello, world! I'm testing the RegexTokenizer.")