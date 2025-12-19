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

        if verbose:
            print('Training completed')
            print('Number of tokens after training: ', sum(len(chunk) for chunk in tokens))
            print('Compression ratio: ', f'{len(text) / sum(len(chunk) for chunk in tokens):.2f}')
    
    def encode(self, text: str) -> list[int]:
        text_chunks = self.compiled_pattern.findall(text)
        tokens = []
        
        for chunk in text_chunks:
            chunk_bytes = chunk.encode('utf-8')
            chunk_tokens = self._encode_chunk(chunk_bytes)
            tokens.extend(chunk_tokens)

        return tokens
    
    def _encode_chunk(self, text_bytes: bytes) -> list[int]:
        tokens = list(text_bytes)
        
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